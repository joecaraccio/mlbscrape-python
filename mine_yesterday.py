import os
from mlbscrape_python.sql.mlb_database import MlbDatabase
from mlbscrape_python.mine.rotowire import RotoWire

os.chdir("/home/cameron/workspaces/MlbDatabase/mlb_scrape/mlbscrape_python")

mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()

RotoWire.mine_yesterdays_results(databaseSession)
databaseSession.close()