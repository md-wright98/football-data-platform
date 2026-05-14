from prefect import flow, task
from match_data_pipeline import download_match_data, transform_match_data, load_match_data_to_bigquery 
import argparse
import logging

dataset_id = "epl_raw"
table_id = "football-data-platform-483422.epl_raw.understat_matches_raw"


@task(retries=3, retry_delay_seconds=60, name="Fetch Match Data")
def task_download(league, season):
  return download_match_data(league, season)


@task(name="Transform Match Data")
def task_transform(raw_match_data, league, season, extracted_at):
  return transform_match_data(raw_match_data, league, season, extracted_at)


@task(retries=3, retry_delay_seconds=60, name="Load Match Data to BigQuery")
def task_upload(transformed_data, table_id):
  return load_match_data_to_bigquery(transformed_data, table_id)


@flow(name="Match Data Pipeline")
def match_data_flow(leagues=['EPL', 'La_Liga', 'Bundesliga', 'Serie_A', 'Ligue_1'], season="2025"):

  for league in leagues:

    raw_match_data, extracted_at = task_download(league=league, season=season)

    if raw_match_data is None:
      print('No data found, terminating flow.')
      continue

    transformed_data = task_transform(
      raw_match_data=raw_match_data, 
      league=league, 
      season=season, 
      extracted_at=extracted_at)
    
    task_upload(transformed_data, table_id)

    logging.info(f"Successfully completed pipeline run for {league} {season}")


if __name__ == "__main__":

  parser = argparse.ArgumentParser(
    description="Run the match data pipeline for a given league and season."
  )

  parser.add_argument(
    "--league",
    type=str,
    nargs='+',
    default=['EPL', 'La_Liga', 'Bundesliga', 'Serie_A', 'Ligue_1'],
    help="League to fetch data for (default: EPL)."
  )

  parser.add_argument(
    "--season",
    type=str,
    default="2025",
    help="Season to fetch data for. Must be the first year of the season, as a string (default: 2025)."
  )

  args = parser.parse_args()

  print("Deploying flow to Prefect Cloud...")
  match_data_flow.serve(
    name="Bi-weekly Match Data Ingestion",
    cron="0 9 * * 2,5",
    parameters={"leagues" : args.league, "season" : args.season}
  )