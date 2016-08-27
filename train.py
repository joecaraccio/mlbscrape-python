from learn.train_network import HitterNetworkTrainer, PitcherNetworkTrainer
from sql.mlb_database import MlbDatabase
from learn.train_regression import HitterRegressionTrainer

databaseSession = MlbDatabase().open_session()

#hitter_network_trainer = HitterNetworkTrainer(databaseSession)
#hitter_network_trainer.train_network()

hitter_regression_trainer = HitterRegressionTrainer(databaseSession)
hitter_regression_trainer.train_network()



#pitcher_network_trainer = PitcherNetworkTrainer(databaseSession)
#pitcher_network_trainer.train_network()

