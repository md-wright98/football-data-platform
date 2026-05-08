import logging
from google.cloud import bigquery

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

client = bigquery.Client()

dataset_id = "epl_raw"
table_id = "understat_matches_raw"

schema = [
  bigquery.SchemaField("match_id", "INT64", mode="REQUIRED"),
  bigquery.SchemaField("league", "STRING", mode="REQUIRED"),
  bigquery.SchemaField("season_start_year", "INT64", mode="REQUIRED"),
  bigquery.SchemaField("extracted_at", "TIMESTAMP", mode="REQUIRED"),
  bigquery.SchemaField("run_id", "STRING", mode="REQUIRED"),
  bigquery.SchemaField("source", "STRING", mode="REQUIRED"),
  bigquery.SchemaField("payload_content_hash", "STRING", mode="NULLABLE"),
  bigquery.SchemaField("payload", "STRING", mode="NULLABLE")
  ]

def setup():
  table_ref = f"{client.project}.{dataset_id}.{table_id}"
  table = bigquery.Table(table_ref, schema=schema)
  client.create_table(table, exists_ok=True)

setup()