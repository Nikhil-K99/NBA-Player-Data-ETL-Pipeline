from pipeline import Pipeline
import requests
import json

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll

pipeline = Pipeline()

def search_player():
    full_name = str(input("Type in the full name of your player:"))
    full_name = full_name.title()
    player_dict = players.get_players()
    try:
        player = [player for player in player_dict if player['full_name'] == full_name ][0]
        player_id = player['id']
        return player_id
    except:
        print("Player not found")
