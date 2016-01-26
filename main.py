
from miner import StatMiner
from mlb_database import MlbDatabase

#TODO: introduce the Player base class
#TODO: add some data for the starting pitcher and catcher giving up stolen bases
#TODO: add hand players pitch with and some data to predict based on this
mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()
#TODO: add some neural networks

statMiner = StatMiner(databaseSession)

statMiner.mine_day("http://mlb.mlb.com/gdcross/components/game/mlb/year_2015/month_07/day_08/")
#statMiner.mine_month("http://mlb.mlb.com/gdcross/components/game/mlb/year_2015/month_06/")
#statMiner.mine_season("2015")

databaseSession.close()

