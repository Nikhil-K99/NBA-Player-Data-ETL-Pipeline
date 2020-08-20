from pipeline import Pipeline
from secrets import password
import pandas as pd
import sqlalchemy
import psycopg2

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll

# instantiate the pipeline
pipeline = Pipeline()

# take in the player desired by the user
full_name = str(input("Type in the full name of your player: "))

#  retrieve the player id from the NBA API
@pipeline.task()
def search_player():
    player_dict = players.get_players()
    try:
        player = [player for player in player_dict if player['full_name'] == full_name ][0]
        playerid = player['id']
        return playerid
    except:
        print("Player not found")

# extract and parse the data from the API using the player id
@pipeline.task(depends_on=search_player)
def get_player_log(playerid):
    gamelog_all = playergamelog.PlayerGameLog(player_id = playerid, season = SeasonAll.all)
    data = gamelog_all.get_data_frames()[0]
    data['GAME_DATE'] = pd.to_datetime(data['GAME_DATE'])
    data['full_name'] = full_name
    drop_cols = ['SEASON_ID','OREB','DREB','PF','PLUS_MINUS','VIDEO_AVAILABLE']
    data.drop(columns = drop_cols, inplace=True)
    return data

# ingest the data into the postgreSQL database
@pipeline.task(depends_on = get_player_log)
def stream_sql(data):
    server = 'postgresql://postgres:' + password + '@localhost/NBA'
    engine = sqlalchemy.create_engine(server)
    con = engine.connect()
    data.to_sql(name = 'player_log',con = con, if_exists = 'append', index = False, chunksize = 500, method = 'multi')
    con.close()

# ingest the player data into a csv file
@pipeline.task(depends_on = get_player_log)
def build_csv(data):
    name = full_name.lower()
    first_name = name.split(' ')[0]
    last_name = name.split(' ')[1]
    file = first_name + '_' + last_name + '.csv'
    data.to_csv(file, index=False)

# run the pipeline 
pipeline.run()
print("The player data has successfully been stored!")
