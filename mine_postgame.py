import os
os.chdir("/home/cameron/workspaces/MlbDatabase/mlb_scrape/Released/mlbscrape_python")
from mlbscrape_python.mine.rotowire import RotoWire
from mlbscrape_python.sql.mlb_database import MlbDatabase

mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()

RotoWire.mine_yesterdays_results(databaseSession)
databaseSession.close()
