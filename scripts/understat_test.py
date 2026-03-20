# import modules
from understatapi import UnderstatClient
from pathlib import Path
import json

# set team, league and season for tests
team = "West Ham"
league = "EPL"
season = "2022"

# set up path and data directory
p = Path("data")
p.mkdir(parents=True, exist_ok=True)



### --- DOWNLOAD SINGLE TEAM SEASON MATCH DATA --- ###
###     Downloads all of the full match for a given team in a given season (each fixture, opponent, result, xG etc.)
#
#team_filename = p / f"understat_team_whu_{season}.json"
#with UnderstatClient() as client:
#  whu_match_data = client.team(team).get_match_data(season=season)
#  with open(team_filename, "w") as f:
#    json.dump(whu_match_data, f, indent=4)



### --- DOWNLOAD ALL PLAYER DATA FOR A SINGLE SEASON --- ###
###     Downloads all of the full season data for every player in a given season (goals, minutes, xG etc.)
#
#player_data_season_filename = p / f"understat_{season}_{league}_players.json"
#with UnderstatClient() as client:
#  player_data_by_season = client.league(league=league).get_player_data(season=season)
#  with open(player_data_season_filename, "w") as f:
#    json.dump(player_data_by_season, f, indent=4)



### --- DOWNLOAD ALL TEAM DATA FOR A SEASON --- ###
###     Download all team data for a given season, full stats on each match they played, much deeper stats but no information on opponent
#
# league_team_filename = p / f"understat_{league}_{season}.json"
# with UnderstatClient() as client:
#  league_team_data = client.league(league=league).get_team_data(season=season)
#  with open(league_team_filename, "w") as f:
#    json.dump(league_team_data, f, indent=4)



### --- DOWNLOAD ALL MATCH DATA FOR A SEASON --- ###
###     Download all match data for a season - every match played, teams involved, result, xGs etc.
#
# league_match_filename = p / f"understat_{league}_{season}_matches.json"
# with UnderstatClient() as client:
#  league_match_data = client.league(league=league).get_match_data(season=season)
#  with open(league_match_filename, "w") as f:
#    json.dump(league_match_data, f, indent=4)



### ---
###    
#
player_season_filename = p / f"understat_{league}_{season}_player.json"
bowen_id = "1776"
with UnderstatClient() as client:
  player_season_data = client.player(player=bowen_id).get_match_data()
  with open(player_season_filename, "w") as f:
    json.dump(player_season_data, f, indent=4)



###
###
#
player_shot_filename = p / f"understat_{league}_{season}_player_shots.json"
bowen_id = "1776"
with UnderstatClient() as client:
  player_shot_data = client.player(player=bowen_id).get_shot_data()
  with open(player_shot_filename, "w") as f:
    json.dump(player_shot_data, f, indent=4)