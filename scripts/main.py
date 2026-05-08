from match_data_pipeline import download_match_data, transform_match_data, load_match_data_to_bigquery 
import argparse
import logging

dataset_id = "epl_raw"
table_id = "football-data-platform-483422.epl_raw.understat_matches_raw"

def main(league: str, season: str):
  
  try:

    raw_match_data, extracted_at = download_match_data(league=league, season=season)

    transformed_data = transform_match_data(
      data=raw_match_data, 
      league=league, 
      season=season, 
      extracted_at_timestamp=extracted_at)
    
    load_match_data_to_bigquery(transformed_data, table_id)

    logging.info(f"Successfully completed pipeline run for {league} {season}")
  
  except Exception as e:
    logging.error(f"Pipeline failed for {league} {season}: {str(e)}")

if __name__ == "__main__":

  parser = argparse.ArgumentParser(
    description="Run the match data pipeline for a given league and season."
  )

  parser.add_argument(
    "--league",
    type=str,
    default="EPL",
    help="League to fetch data for (default: EPL)."
  )

  parser.add_argument(
    "--season",
    type=str,
    default="2025",
    help="Season to fetch data for. Must be the first year of the season, as a string (default: 2025)."
  )

  args = parser.parse_args()

  main(league=args.league, season=args.season)