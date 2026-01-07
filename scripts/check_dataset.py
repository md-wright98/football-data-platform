from google.cloud import bigquery

client = bigquery.Client()
dataset_id = "epl_raw"

dataset = client.get_dataset(f"{client.project}.{dataset_id}")
print(dataset.full_dataset_id, dataset.location)