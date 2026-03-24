from google.cloud import bigquery

client = bigquery.Client()

query = "SELECT 1 AS ok"
result = client.query(query).result()

for row in result:
  print(row["ok"])