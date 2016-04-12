
from miner import StatMiner
from mlb_database import MlbDatabase
from rotowire import RotoWire
import os

os.chdir("/home/cameron/workspaces/MlbDatabase/mlb_scrape/mlbscrape-python")

#TODO: add some data for the starting pitcher and catcher giving up stolen bases
mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()
# TODO: enable GPU support

statMiner = StatMiner(databaseSession)
RotoWire.get_lineups()
#statMiner.mine_yesterday()
#statMiner.mine_day(4, 10, 2016)
#statMiner.mine_day("http://mlb.mlb.com/gdcross/components/game/mlb/year_2015/month_05/day_10/")
#statMiner.mine_month("http://mlb.mlb.com/gdcross/components/game/mlb/year_2015/month_05/")
#statMiner.mine_season("2015")

databaseSession.close()

