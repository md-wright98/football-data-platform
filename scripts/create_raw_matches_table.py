from google.cloud import bigquery

client = bigquery.Client()

dataset_id = "epl_raw"
table_id = "understat_matches_raw"

table_ref = f"{client.project}.{dataset_id}.{table_id}"
print("Target table:", table_ref)

schema = [
  bigquery.SchemaField("match_id", "INT64", mode="REQUIRED"),
  bigquery.SchemaField("league", "STRING", mode="REQUIRED"),
  bigquery.SchemaField("season_start_year", "INT64", mode="REQUIRED"),
  bigquery.SchemaField("extracted_at", "TIMESTAMP", mode="REQUIRED"),
  bigquery.SchemaField("ingested_at", "TIMESTAMP", mode="REQUIRED"),
  bigquery.SchemaField("run_id", "INT64", mode="REQUIRED"),
  bigquery.SchemaField("source", "STRING", mode="REQUIRED"),
  bigquery.SchemaField("payload_content_hash", "STRING", mode="NULLABLE"),
  bigquery.SchemaField("payload", "JSON", mode="NULLABLE")
  ]

table = bigquery.Table(table_ref, schema=schema)

try:
  table = client.create_table(table, exists_ok=True)
  print("Table ready:", table.full_table_id)
except:
  print("CREATE TABLE FAILED:")
  raise