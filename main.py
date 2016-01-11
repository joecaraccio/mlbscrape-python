
from miner import StatMiner
from mlb_database import MlbDatabase

#TODO: sessions should be initiated here
mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()
#TODO: add some neural networks

statMiner = StatMiner(databaseSession)

statMiner.mine_day("http://mlb.mlb.com/gdcross/components/game/mlb/year_2015/month_07/day_01/")
#statMiner.mine_month("http://mlb.mlb.com/gdcross/components/game/mlb/year_2015/month_06/")
#statMiner.mine_season("2015")

databaseSession.close()

