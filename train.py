from mlbscrape_python.learn.train_network import HitterNetworkTrainer, PitcherNetworkTrainer
from mlbscrape_python.sql.mlb_database import MlbDatabase

mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()

hitter_network_trainer = HitterNetworkTrainer(databaseSession)
hitter_network_trainer.train_network()


pitcher_network_trainer = PitcherNetworkTrainer(databaseSession)
pitcher_network_trainer.train_network()

