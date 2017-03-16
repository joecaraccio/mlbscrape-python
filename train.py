from learn.train_network import HitterNetworkTrainer, PitcherNetworkTrainer
from sql.mlb_database import MlbDatabase
from learn.train_regression import *

databaseSession = MlbDatabase().open_session()

hitter_regression_trainer = HitterRegressionForestTrainer()
hitter_regression_trainer.train_network()

