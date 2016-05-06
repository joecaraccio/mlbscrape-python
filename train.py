from mlbscrape_python.learn.train_network import HitterNetworkTrainer
from mlbscrape_python.sql.mlb_database import MlbDatabase

mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()

network_trainer = HitterNetworkTrainer(databaseSession)
network_trainer.train_network()
