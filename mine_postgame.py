
from sql.mlb_database import MlbDatabase
from mine.rotowire import mine_game_results
from datetime import date, timedelta

mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()

mine_game_results(databaseSession, date.today()-timedelta(1))
databaseSession.close()
