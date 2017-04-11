
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import tree
import random
from sql.pregame_hitter import PregameHitterGameEntry
from sql.pregame_pitcher import PregamePitcherGameEntry
from sql.postgame_hitter import PostgameHitterGameEntry
from sql.postgame_pitcher import PostgamePitcherGameEntry
from sql.mlb_database import MlbDatabase
from sql.umpire import UmpireCareerEntry
from sqlalchemy.orm.exc import NoResultFound
from sklearn.externals.six import StringIO
import pydotplus
import numpy as np
#from mine.stat_miner import UmpireMiner
from sql.team_park import ParkEntry
import datetime
from datetime import timedelta
from sklearn.metrics import mean_squared_error, median_absolute_error


class RegressionTree(object):
    def __init__(self):
        self._decision_tree = DecisionTreeRegressor()
        self._database_session = MlbDatabase().open_session()

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

    def _save_model(self):
        """ Pure virtual method for saving the final model
        """
        assert 0


class RegressionForest(object):
    def __init__(self):
        self._decision_tree = RandomForestRegressor(n_estimators=1000)
        self._database_session = MlbDatabase().open_session()

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

    def _save_model(self):
        """ Pure virtual method for saving the final model
        """
        assert 0


class HitterRegressionTrainer(RegressionTree):

    SIZE_TRAINING_BATCH = 2000

    def get_stochastic_batch(self, input_query, num_samples):
        player_samples = random.sample([itm for itm in input_query], num_samples)
        x = list()
        y = list()
        for item in player_samples:
            input_vector = item.to_input_vector()
            postgame_entry = self._database_session.query(PostgameHitterGameEntry).get((item.rotowire_id,
                                                                                        item.game_date,
                                                                                        item.game_time))
            if postgame_entry is None:
                continue

            if postgame_entry.game_entry.umpire is None:
                umpire_vector = UmpireCareerEntry.get_nominal_data(self._database_session)
            else:
                umpire_vector = postgame_entry.game_entry.umpire_object.to_input_vector()

            game_datetime = datetime.strptime(item.game_date, "yyyy-mm-dd")
            park_factors = self._database_session.query(ParkEntry).get((item.home_team, str(game_datetime.year-1)))
            park_vector = park_factors.to_input_vector()

            final_hitter_array = np.concatenate([input_vector, park_vector, umpire_vector])
            x.append(final_hitter_array.tolist())
            y.append([postgame_entry.actual_draftkings_points])

        return x, y

    def train_network(self):
        """ Pure virtual method for training the network
        """
        db_query = self._database_session.query(PregameHitterGameEntry)
        mlb_training_data, mlb_evaluation_data = self.get_train_eval_data(db_query, 0.8)
        x_train, y_train = self.get_stochastic_batch(mlb_training_data, self.SIZE_TRAINING_BATCH)
        self._decision_tree.fit(x_train, y_train)
        dot_data = StringIO()
        tree.export_graphviz(self._decision_tree, out_file=dot_data,
                             feature_names=PregameHitterGameEntry.get_input_vector_labels())
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph.write_pdf("hitter_tree.pdf")
        x_test_actual = list()
        y_test_actual = list()
        for data in mlb_evaluation_data:
            postgame_entry = self._database_session.query(PostgameHitterGameEntry).get((data.rotowire_id,
                                                                                       data.game_date,
                                                                                       data.game_time))
            if postgame_entry is None:
                print "Ignoring hitter %s since his postgame stats were not found." % data.rotowire_id
                continue

            y_test_actual.append([postgame_entry.actual_draftkings_points])
            x_test_actual.append(data.to_input_vector())

        self._database_session.close()

    def get_prediction(self, input_data):
        return self._decision_tree.predict([input_data])


class HitterRegressionForestTrainer(RegressionForest):

    SIZE_TRAINING_BATCH = 7000

    def get_stochastic_batch(self, input_query, num_samples=None):
        potential_samples = list()
        for postgame_entry in input_query:
            pregame_entry = self._database_session.query(PregameHitterGameEntry).get((postgame_entry.rotowire_id,
                                                                                       postgame_entry.game_date,
                                                                                       postgame_entry.game_time))
            if pregame_entry is not None:
                potential_samples.append((pregame_entry, postgame_entry))
            else:
                print "Can't find %s %s %s %s" % (postgame_entry.rotowire_id, postgame_entry.home_team,
                                                  postgame_entry.game_date, postgame_entry.game_time)
        if num_samples is None:
            num_samples = len(potential_samples)
        player_samples = random.sample([itm for itm in potential_samples], num_samples)
        x = list()
        y = list()
        for item in player_samples:
            pregame_entry = item[0]
            postgame_entry = item[1]
            input_vector = pregame_entry.to_input_vector()

            if pregame_entry.game_entry is None:
                print "NoneType game entry for %s %s %s %s" % (pregame_entry.rotowire_id, pregame_entry.home_team,
                                                               pregame_entry.game_date, pregame_entry.game_time)
                continue

            if pregame_entry.game_entry.umpire is None:
                umpire_vector = UmpireCareerEntry.get_nominal_data(self._database_session)
            else:
                ump_entry = self._database_session.query(UmpireCareerEntry).get(pregame_entry.game_entry.umpire)

                if ump_entry is None:
                    umpire_vector = UmpireCareerEntry.get_nominal_data(self._database_session)
                else:
                    umpire_vector = ump_entry.to_input_vector()

            game_datetime = datetime.datetime.strptime(pregame_entry.game_date, "%Y-%m-%d")
            park_factors = self._database_session.query(ParkEntry).get((pregame_entry.home_team, "2016"))
            if park_factors is None:
                print "Hitter regression forest: Could not find %s from %s" % (pregame_entry.home_team, "2016")
                park_vector = np.array([100, 100])
            else:
                park_vector = park_factors.to_input_vector()

            final_pitcher_array = np.concatenate([input_vector, park_vector, umpire_vector])
            x.append(final_pitcher_array.tolist())
            y.append([postgame_entry.actual_draftkings_points])

        return x, y

    def train_network(self):
        """ Pure virtual method for training the network
        """
        db_query = self._database_session.query(PostgameHitterGameEntry)
        mlb_training_data, mlb_evaluation_data = self.get_train_eval_data(db_query, 0.8)
        x_train, y_train = self.get_stochastic_batch(mlb_training_data)
        self._decision_tree.fit(x_train, np.ravel(y_train))
        x_eval, y_eval = self.get_stochastic_batch(mlb_evaluation_data)
        y_eval_predictions = self._decision_tree.predict(x_eval)
        y_eval_predictions = np.array(y_eval_predictions)
        y_eval = np.array(y_eval)
        print "Hitter Training Size: %i | Hitter Evaluation Size: %i" % (len(x_train), len(x_eval))
        print "Hitter median absolute error: %f" % median_absolute_error(y_eval, y_eval_predictions)
        self._database_session.close()

    def get_prediction(self, input_data):
        return self._decision_tree.predict([input_data])


class PitcherRegressionTrainer(RegressionTree):

    SIZE_TRAINING_BATCH = 300

    def get_stochastic_batch(self, input_query, num_samples):
        player_samples = random.sample([itm for itm in input_query], num_samples)
        x = list()
        y = list()
        for item in player_samples:
            input_vector = item.to_input_vector()
            postgame_entry = self._database_session.query(PostgamePitcherGameEntry).get((item.rotowire_id,
                                                                                         item.game_date,
                                                                                         item.game_time))
            if postgame_entry is None:
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
        x_train, y_train = self.get_stochastic_batch(mlb_training_data, self.SIZE_TRAINING_BATCH)
        self._decision_tree.fit(x_train, y_train)
        dot_data = StringIO()
        tree.export_graphviz(self._decision_tree, out_file=dot_data,
                             feature_names=PregamePitcherGameEntry.get_input_vector_labels())
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph.write_pdf("pitcher_tree.pdf")
        x_test_actual = list()
        y_test_actual = list()
        for data in mlb_evaluation_data:
            postgame_entry = self._database_session.query(PostgamePitcherGameEntry).get((data.rotowire_id,
                                                                                         data.game_date,
                                                                                         data.game_time))

            if postgame_entry is None:
                print "Ignoring hitter %s since his postgame stats were not found." % data.rotowire_id
                continue

            y_test_actual.append([postgame_entry.actual_draftkings_points])
            x_test_actual.append(data.to_input_vector())

        self._database_session.close()

    def get_prediction(self, input_data):
        return self._decision_tree.predict([input_data])


class PitcherRegressionForestTrainer(RegressionForest):

    SIZE_TRAINING_BATCH = 900

    def get_stochastic_batch(self, input_query, num_samples=None):
        potential_samples = list()
        for postgame_entry in input_query:
            pregame_entry = self._database_session.query(PregamePitcherGameEntry).get((postgame_entry.rotowire_id,
                                                                                       postgame_entry.game_date,
                                                                                       postgame_entry.game_time))
            if pregame_entry is not None:
                potential_samples.append((pregame_entry, postgame_entry))
            else:
                print "Can't find %s %s %s %s" % (postgame_entry.rotowire_id, postgame_entry.home_team,
                                                  postgame_entry.game_date, postgame_entry.game_time)
        if num_samples is None:
            num_samples = len(potential_samples)
        player_samples = random.sample([itm for itm in potential_samples], num_samples)
        x = list()
        y = list()
        for item in player_samples:
            pregame_entry = item[0]
            postgame_entry = item[1]
            input_vector = pregame_entry.to_input_vector()

            if pregame_entry.game_entry is None:
                print "NoneType game entry for %s %s %s %s" % (pregame_entry.rotowire_id, pregame_entry.home_team,
                                                               pregame_entry.game_date, pregame_entry.game_time)
                continue

            if pregame_entry.game_entry.umpire is None:
                umpire_vector = UmpireCareerEntry.get_nominal_data(self._database_session)
            else:
                ump_entry = self._database_session.query(UmpireCareerEntry).get(pregame_entry.game_entry.umpire)

                if ump_entry is None:
                    umpire_vector = UmpireCareerEntry.get_nominal_data(self._database_session)
                else:
                    umpire_vector = ump_entry.to_input_vector()

            game_datetime = datetime.datetime.strptime(pregame_entry.game_date, "%Y-%m-%d")
            park_factors = self._database_session.query(ParkEntry).get((pregame_entry.home_team, "2016"))
            if park_factors is None:
                print "Pitcher regression forest: Could not find %s from %s" % (pregame_entry.home_team, "2016")
                park_vector = np.array([100, 100])
            else:
                park_vector = park_factors.to_input_vector()

            final_pitcher_array = np.concatenate([input_vector, pregame_entry.get_opponent_vector(), park_vector, umpire_vector])
            x.append(final_pitcher_array.tolist())
            y.append([postgame_entry.actual_draftkings_points])

        return x, y

    def train_network(self):
        """ Pure virtual method for training the network
        """
        db_query = self._database_session.query(PostgamePitcherGameEntry)
        mlb_training_data, mlb_evaluation_data = self.get_train_eval_data(db_query, 0.8)
        x_train, y_train = self.get_stochastic_batch(mlb_training_data)
        self._decision_tree.fit(x_train, np.ravel(y_train))
        x_eval, y_eval = self.get_stochastic_batch(mlb_evaluation_data)
        y_eval_predictions = self._decision_tree.predict(x_eval)
        y_eval_predictions = np.array(y_eval_predictions)
        y_eval = np.array(y_eval)
        print "Pitcher Training Size: %i | Pitcher Evaluation Size: %i" % (len(x_train), len(x_eval))
        print "Pitcher median absolute error: %f" % median_absolute_error(y_eval, y_eval_predictions)
        self._database_session.close()

    def get_prediction(self, input_data):
        return self._decision_tree.predict([input_data])
