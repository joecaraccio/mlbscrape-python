
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import random
from sql.pregame_hitter import PregameHitterGameEntry
from sql.pregame_pitcher import PregamePitcherGameEntry
from sql.postgame_hitter import PostgameHitterGameEntry
from sql.postgame_pitcher import PostgamePitcherGameEntry
from sqlalchemy.orm.exc import NoResultFound


class HitterRegressionTrainer(object):

    SIZE_TRAINING_BATCH = 2000

    def __init__(self, database_session):
        self._database_session = database_session

    @staticmethod
    def get_train_eval_data(db_query, training_pct):
        """ Get the training data and evaluation data from a SQLAlchemy query
        :param db_query: a SQLAlchemy Query object
        :param training_pct: percentage of data to be dedicated to training
        :return: list of training data, list of evaluation data
        """
        new_query = [itm for itm in db_query]
        random.shuffle(new_query)
        training_data = new_query[0:int(round(len(new_query)*training_pct))-1]
        evaluation_data = new_query[int(round(len(new_query)*training_pct))-1:len(new_query)-1]

        return training_data, evaluation_data

    def get_stochastic_batch(self, input_query, num_samples):
        player_samples = random.sample([itm for itm in input_query], num_samples)
        x = list()
        y = list()
        for item in player_samples:
            input_vector = item.to_input_vector()
            try:
                postgame_entry = self._database_session.query(PostgameHitterGameEntry).filter(PostgameHitterGameEntry.rotowire_id == item.rotowire_id,
                                                                                              PostgameHitterGameEntry.game_date == item.game_date).one()
            except NoResultFound:
                #print "Ignoring hitter %s since his postgame stats were not found." % item.rotowire_id
                continue

            x.append(input_vector)
            y.append([postgame_entry.actual_draftkings_points])

        return x, y

    def _save_model(self):
        """ Pure virtual method for saving the final model
        """
        assert 0

    def train_network(self):
        """ Pure virtual method for training the network
        """
        db_query = self._database_session.query(PregameHitterGameEntry)
        mlb_training_data, mlb_evaluation_data = self.get_train_eval_data(db_query, 0.8)
        X_train, Y_train = self.get_stochastic_batch(mlb_training_data, self.SIZE_TRAINING_BATCH)
        self._decision_tree = DecisionTreeRegressor()
        self._decision_tree.fit(X_train, Y_train)

        X_test_actual = list()
        Y_test_actual = list()
        for data in mlb_evaluation_data:
            try:
                postgame_entry = self._database_session.query(PostgameHitterGameEntry).filter(PostgameHitterGameEntry.rotowire_id == data.rotowire_id,
                                                                                              PostgameHitterGameEntry.game_date == data.game_date).one()
                Y_test_actual.append([postgame_entry.actual_draftkings_points])
                X_test_actual.append(data.to_input_vector())
            except NoResultFound:
                print "Ignoring hitter %s since his postgame stats were not found." % data.rotowire_id
                continue

    def get_prediction(self, input_data):
        return self._decision_tree.predict([input_data])


class PitcherRegressionTrainer(object):

    SIZE_TRAINING_BATCH = 300

    def __init__(self, database_session):
        self._database_session = database_session

    @staticmethod
    def get_train_eval_data(db_query, training_pct):
        """ Get the training data and evaluation data from a SQLAlchemy query
        :param db_query: a SQLAlchemy Query object
        :param training_pct: percentage of data to be dedicated to training
        :return: list of training data, list of evaluation data
        """
        new_query = [itm for itm in db_query]
        random.shuffle(new_query)
        training_data = new_query[0:int(round(len(new_query)*training_pct))-1]
        evaluation_data = new_query[int(round(len(new_query)*training_pct))-1:len(new_query)-1]

        return training_data, evaluation_data

    def get_stochastic_batch(self, input_query, num_samples):
        player_samples = random.sample([itm for itm in input_query], num_samples)
        x = list()
        y = list()
        for item in player_samples:
            input_vector = item.to_input_vector()
            try:
                postgame_entry = self._database_session.query(PostgamePitcherGameEntry).filter(PostgamePitcherGameEntry.rotowire_id == item.rotowire_id,
                                                                                              PostgamePitcherGameEntry.game_date == item.game_date).one()
            except NoResultFound:
                #print "Ignoring hitter %s since his postgame stats were not found." % item.rotowire_id
                continue

            x.append(input_vector)
            y.append([postgame_entry.actual_draftkings_points])

        return x, y

    def _save_model(self):
        """ Pure virtual method for saving the final model
        """
        assert 0

    def train_network(self):
        """ Pure virtual method for training the network
        """
        db_query = self._database_session.query(PregamePitcherGameEntry)
        mlb_training_data, mlb_evaluation_data = self.get_train_eval_data(db_query, 0.8)
        X_train, Y_train = self.get_stochastic_batch(mlb_training_data, self.SIZE_TRAINING_BATCH)
        self._decision_tree = DecisionTreeRegressor()
        self._decision_tree.fit(X_train, Y_train)

        X_test_actual = list()
        Y_test_actual = list()
        for data in mlb_evaluation_data:
            try:
                postgame_entry = self._database_session.query(PostgamePitcherGameEntry).filter(PostgamePitcherGameEntry.rotowire_id == data.rotowire_id,
                                                                                              PostgamePitcherGameEntry.game_date == data.game_date).one()
                Y_test_actual.append([postgame_entry.actual_draftkings_points])
                X_test_actual.append(data.to_input_vector())
            except NoResultFound:
                print "Ignoring hitter %s since his postgame stats were not found." % data.rotowire_id
                continue

    def get_prediction(self, input_data):
        return self._decision_tree.predict([input_data])

