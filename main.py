import os

from mine.miner import StatMiner
from sql.mlb_database import MlbDatabase
from mine.rotowire import RotoWire
from mlbscrape_python.mine.draft_kings import Draftkings

os.chdir("/home/cameron/workspaces/MlbDatabase/mlb_scrape/mlbscrape_python")

#TODO: add some data for the starting pitcher and catcher giving up stolen bases
mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()
# TODO: enable GPU support

statMiner = StatMiner(databaseSession)
RotoWire.mine_pregame_stats(databaseSession)
Draftkings.save_daily_csv()

databaseSession.close()

