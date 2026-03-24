# imports
from understatapi import UnderstatClient
from datetime import datetime
from google.cloud import bigquery
# import logging
import json
import hashlib
import uuid
import pandas as pd 

# create BigQuery client object
client = bigquery.Client()

# set dataset_id and table_id
dataset_id = "epl_raw"
table_id = "football-data-platform-483422.epl_raw.understat_matches_landing"

# 1. Download match data and generate an extraction timestamp
def download_match_data(league: str, season: str) -> dict:

  print(f"Starting match data download for {league} {season} season.")
  #logger.info(f"Starting match data download for {league} {season} season.")

  try:
    with UnderstatClient() as understat_client:
      match_data = UnderstatClient().league(league=league).get_match_data(season=season)
      extracted_at_timestamp = datetime.now()
      print(f"Downloaded data for {len(match_data)} matches.")
      #logging.info(f"Downloaded data for {len(match_data)} matches.")
  except Exception:
    print(f"Failed to download match data for {league} {season} season.")
    #logger.exception(f"Failed to download match data for {league} {season} season.")
    raise

  return match_data, extracted_at_timestamp


# 2. Transform each match entry into a row for the raw layer
def transform_match_data(data: dict, league: str, season: str, extracted_at_timestamp) -> list:

  match_rows = []

  def create_hash(match_data: dict) -> str:
    canonical = json.dumps(match_data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

  for match in data:

    row = {
      # a. extract the match_id into its own column
      "match_id" : int(match["id"]),
      # b. store the leage 
      "league" : league,
      # c. store the season in its own column
      "season_start_year" : int(season),
      # d. store the ingested_at_timestamp
      "extracted_at" : extracted_at_timestamp,
      # e. create ingested_at_timestamp at ingestion
      "ingested_at" : None,
      # f. store the run ID from point of ingestion as its own column
      "run_id" : f"{extracted_at_timestamp.strftime('%Y%m%dT%H%M%S')}_{uuid.uuid4().hex[:8]}",
      # g. store Understat as the source
      "source" : "Understat",
      # h. create a hash for the JSON payload for idempotency purposes
      "payload_content_hash" : create_hash(match),
      # i. store the JSON payload for the match
      "payload" : json.dumps(match)
    }

    match_rows.append(row)

  match_df = pd.DataFrame.from_dict(data=match_rows)

  return match_df


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
    ]
  )

  job = client.load_table_from_dataframe(dataframe=data, destination=table_id, job_config=job_config)
  job.result()

  table = client.get_table(table_id)
  print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id} table.")


# 4. Load each row into BigQuery
  # a. generate a timestamp at the point of ingestion

# main(season, league)
  #raw_data, timestamp = download_match_data(season, league)
  
  # run_id = generate_run_id
  #transform_match_data("2021", raw_data, timestamp)
    # generate_payload_hash
  # load_data_to_bigquery
    # generate_ingested_at_timestamp

raw_data, extracted_at = download_match_data(league="EPL", season="2021")
transformed_data = transform_match_data(data=raw_data, league="EPL", season="2021", extracted_at_timestamp=extracted_at)
load_match_data_to_bigquery(transformed_data, table_id)