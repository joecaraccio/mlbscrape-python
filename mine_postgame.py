
from sql.mlb_database import MlbDatabase
from mine.rotowire import mine_yesterdays_results

mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()

mine_yesterdays_results(databaseSession)
databaseSession.close()
