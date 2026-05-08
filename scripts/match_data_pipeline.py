# imports
import logging
import json
import hashlib
import uuid
import pandas as pd 
from understatapi import UnderstatClient
from datetime import datetime, timezone
from google.cloud import bigquery

# Setup logging
logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# create BigQuery client object
client = bigquery.Client()

# set dataset_id and table_id

CONFIG = {

  "dataset_id" : "epl_raw",
  "table_id" : "football-data-platform-483422.epl_raw.understat_matches_raw",

}

# 1. Download match data and generate an extraction timestamp
def download_match_data(league: str, season: str) -> tuple[list, datetime]:
  """
  Fetches raw match data from Understat for a specific league and season.

  Args:
    league (str): Name of league as a string e.g. 'EPL'
    season (str): Start year of season as a string e.g. '2025'

  Returns:
    tuple: (list of match dictionaries, extraction timestamp)
  """
  logger.info(f"Starting match data download for {league} {season} season.")

  try:
    with UnderstatClient() as understat:
      match_data = UnderstatClient().league(league=league).get_match_data(season=season)
      extracted_at_timestamp = datetime.now(timezone.utc)
      logging.info(f"Succesfully downloaded {len(match_data)} matches for {league} {season}.")
      return match_data, extracted_at_timestamp
  except Exception as e:
    logger.error(f"Failed to download match data for {league} {season}: {str(e)}")
    raise

# 2. Transform each match entry into a row for the raw layer
def transform_match_data(data: dict, league: str, season: str, extracted_at_timestamp) -> pd.DataFrame:
  """
  Cleans and structures raw Understat API data into format suitable for BigQuery. Includes a content hash
  for idempotency and a batch run ID for traceability.
  """
  def create_hash(match_data: dict) -> str:
    canonical = json.dumps(match_data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

  match_rows = []
  batch_run_id = f"{extracted_at_timestamp.strftime('%Y%m%dT%H%M%S')}_{uuid.uuid4().hex[:8]}"

  try:

    for match in data:
      match_rows.append({
        # a. extract the match_id into its own column
        "match_id" : int(match["id"]),
        # b. store the leage 
        "league" : league,
        # c. store the season in its own column
        "season_start_year" : int(season),
        # d. store the ingested_at_timestamp
        "extracted_at" : extracted_at_timestamp,
        # f. store the run ID from point of ingestion as its own column
        "run_id" : batch_run_id,
        # g. store Understat as the source
        "source" : "Understat",
        # h. create a hash for the JSON payload for idempotency purposes
        "payload_content_hash" : create_hash(match),
        # i. store the JSON payload for the match
        "payload" : json.dumps(match)
    })
      
    logger.info(f"Transformed {len(match_rows)} rows for {league} {season}.")
    return pd.DataFrame.from_dict(data=match_rows)

  except KeyError as e:
    logger.error(f"Data structure error in transformation: Missing key {e}")
    raise


def load_match_data_to_bigquery(data, table_id):

  job_config = bigquery.LoadJobConfig(
    schema=[
      bigquery.SchemaField("match_id", "INT64", mode="REQUIRED"),
      bigquery.SchemaField("league", "STRING", mode="REQUIRED"),
      bigquery.SchemaField("season_start_year", "INT64", mode="REQUIRED"),
      bigquery.SchemaField("extracted_at", "TIMESTAMP", mode="REQUIRED"),
      bigquery.SchemaField("run_id", "STRING", mode="REQUIRED"),
      bigquery.SchemaField("source", "STRING", mode="REQUIRED"),
      bigquery.SchemaField("payload_content_hash", "STRING", mode="NULLABLE"),
      bigquery.SchemaField("payload", "STRING", mode="NULLABLE")
    ],
    write_disposition="WRITE_APPEND"
  )

  try:
    logger.info(f"Loading data to {table_id}...")
    job = client.load_table_from_dataframe(dataframe=data, destination=table_id, job_config=job_config)
    job.result()
    logger.info(f"Job complete. Loaded to {table_id}")
  except Exception as e:
    print(f"BigQuery load failed: {e}")
    raise