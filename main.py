
from miner import StatMiner
from mlb_database import MlbDatabase

#TODO: change the addition of HitterEntrys to check the date update first
#TODO: add pitchers
#TODO: add some data for the starting pitcher and catcher giving up stolen bases
mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()
#TODO: add some neural networks

statMiner = StatMiner(databaseSession)

statMiner.mine_day("http://mlb.mlb.com/gdcross/components/game/mlb/year_2015/month_09/day_01/")
#statMiner.mine_month("http://mlb.mlb.com/gdcross/components/game/mlb/year_2015/month_06/")
#statMiner.mine_season("2015")

databaseSession.close()

