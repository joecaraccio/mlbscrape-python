import random

import numpy as np
import tensorflow as tf
from Released.mlbscrape_python.sql.pregame_hitter import PregameHitterGameEntry
from Released.mlbscrape_python.sql.postgame_hitter import PostgameHitterGameEntry
from Released.mlbscrape_python.sql.pregame_pitcher import PregamePitcherGameEntry
from Released.mlbscrape_python.sql.postgame_pitcher import PostgamePitcherGameEntry
from sqlalchemy.orm.exc import NoResultFound
import csv


class NetworkTrainer(object):

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

    def train_network(self):
        """ Pure virtual method for training the network
        """
        assert 0

    def get_prediction(self, input_data):
        """ Pure virtual method for generating the output given inputs
        :param input_data: the input data needed to generate output in this network
        :return: the output prediction
        """
        assert 0


class HitterNetworkTrainer(NetworkTrainer):

    TRAINING_ITERATIONS = 300
    SIZE_TRAINING_BATCH = 250

    def __init__(self, database_session):
        self._database_session = database_session

    @staticmethod
    def get_batting_order_offset(order_number, offset_value):
        batting_position = order_number + offset_value
        if order_number > 9:
            return 1
        elif order_number < 1:
            return 9
        else:
            return batting_position

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

    def train_network(self):
        """ Train the network using the database date and write the result to a CSV file for now
        """
        db_query = self._database_session.query(PregameHitterGameEntry)
        mlb_training_data, mlb_evaluation_data = self.get_train_eval_data(db_query, 0.8)

        # y = x*w + b
        input_dimension = len(mlb_training_data[0].to_input_vector())
        x = tf.placeholder(tf.float32, [None, input_dimension])
        #w = tf.Variable(tf.zeros([input_dimension, 1]))
        w1 = tf.Variable(tf.zeros([input_dimension, 1]))
        #w2 = tf.Variable(tf.zeros([5, 1]))
        b = tf.Variable(tf.zeros([1, input_dimension]))
        #y = tf.nn.relu(tf.matmul(x, w1) + b)
        y = tf.add(tf.matmul(x, w1), b)

        # Actual Draftkings points
        y_ = tf.placeholder(tf.float32, [None, 1])

        # Minimize the square error
        square_error = tf.square(y_ - y)
        train_step = tf.train.AdamOptimizer(0.0001).minimize(square_error)

        # Initialize all TensorFlow variables
        init = tf.initialize_all_variables()
        sess = tf.Session()
        sess.run(init)

        # Perform the actual training of the net
        # Stochastic training with 100 instances run 1000 times
        for i in range(HitterNetworkTrainer.TRAINING_ITERATIONS):
            batch_xs, batch_ys = self.get_stochastic_batch(mlb_training_data, HitterNetworkTrainer.SIZE_TRAINING_BATCH)
            batch_xs = np.array(batch_xs, dtype=float)
            batch_ys = np.array(batch_ys, dtype=float)
            sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
            print "Training Iteration %i" % i

        # Save the weights to a file
        with open('hitter_weights.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow("w1")
            for weight in w1.eval(sess):
                spamwriter.writerow(weight)
            """spamwriter.writerow("w2")
            for weight in w2.eval(sess):
                spamwriter.writerow(weight)
            """
            spamwriter.writerow("b")
            for bias in np.transpose(b.eval(sess)):
                spamwriter.writerow(bias)

        test_data_input = list()
        test_data_output = list()
        for data in mlb_evaluation_data:
            try:
                postgame_entry = self._database_session.query(PostgameHitterGameEntry).filter(PostgameHitterGameEntry.rotowire_id == data.rotowire_id,
                                                                                              PostgameHitterGameEntry.game_date == data.game_date).one()
                test_data_output.append([postgame_entry.actual_draftkings_points])
                test_data_input.append(data.to_input_vector())
            except NoResultFound:
                print "Ignoring hitter %s since his postgame stats were not found." % data.rotowire_id
                continue

        test_data_input = np.array(test_data_input, dtype=float)
        print "Input data shape: " + str(test_data_input.shape)
        test_data_output = np.array(test_data_output, dtype=float)
        print "Output data shape: " + str(test_data_output.shape)
        difference_prediction = tf.reduce_mean(tf.sqrt(tf.square(y-y_)))
        print (sess.run(difference_prediction, feed_dict={x: test_data_input, y_: test_data_output}))

    @staticmethod
    def get_prediction(input_data):
        # Load the weights from the file, evaluate the output using numpy
        # Save the weights to a file
        model_weights1 = list()
        weights_file = open('hitter_weights.csv', 'rb')
        spamreader = csv.reader(weights_file, delimiter=',')
        for weight in spamreader:
            if weight == "b":
                break
            model_weights1.append(weight[0])
        if len(input_data) != len(model_weights1):
            return 0
        """model_weights2 = list()
        for weight in spamreader:
            if weight == "b":
                break
            model_weights2.append(weight[0])
        """
        biases = list()
        for bias in spamreader:
            biases.append(bias[0])
        weights_file.close()
        if len(input_data) != len(biases):
            return 0

        model_weight_array1 = np.array(model_weights1, dtype=float)
        input_data_array = np.array(input_data, dtype=float)
        return np.add(np.matmul(model_weight_array1, input_data_array), np.array(biases, dtype=float))


class PitcherNetworkTrainer(NetworkTrainer):

    TRAINING_ITERATIONS = 1000
    SIZE_TRAINING_BATCH = 100

    def __init__(self, database_session):
        self._database_session = database_session

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
                continue

            x.append(input_vector)
            y.append([postgame_entry.actual_draftkings_points])

        return x, y

    def train_network(self):
        """ Train the network using the database date and write the result to a CSV file for now
        """
        db_query = self._database_session.query(PregamePitcherGameEntry)
        mlb_training_data, mlb_evaluation_data = self.get_train_eval_data(db_query, 0.8)

        # y = x*w + b
        x = tf.placeholder(tf.float32, [None, 31*1])
        w = tf.Variable(tf.zeros([31*1, 1]))
        b = tf.Variable(tf.zeros([1, 31*1]))
        y = tf.reduce_sum(tf.matmul(x, w) + b, 1)

        # Actual Draftkings points
        y_ = tf.placeholder(tf.float32, [None, 1])

        # Minimize the square error
        square_error = tf.square(y_ - y)
        train_step = tf.train.AdamOptimizer(0.0001).minimize(square_error)

        # Initialize all TensorFlow variables
        init = tf.initialize_all_variables()
        sess = tf.Session()
        sess.run(init)

        # Perform the actual training of the net
        # Stochastic training with 100 instances run 1000 times
        for i in range(PitcherNetworkTrainer.TRAINING_ITERATIONS):
            batch_xs, batch_ys = self.get_stochastic_batch(mlb_training_data, PitcherNetworkTrainer.SIZE_TRAINING_BATCH)
            batch_xs = np.array(batch_xs, dtype=float)
            batch_ys = np.array(batch_ys, dtype=float)
            sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
            print "Training Iteration %i" % i

        # Save the weights to a file
        with open('pitcher_weights.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            for weight in w.eval(sess):
                spamwriter.writerow(weight)

        test_data_input = list()
        test_data_output = list()
        for data in mlb_evaluation_data:
            test_data_input.append(data.to_input_vector())
            try:
                postgame_entry = self._database_session.query(PostgamePitcherGameEntry).filter(PostgamePitcherGameEntry.rotowire_id == data.rotowire_id,
                                                                                               PostgamePitcherGameEntry.game_date == data.game_date).one()
                test_data_output.append([postgame_entry.actual_draftkings_points])
            except NoResultFound:
                continue

        test_data_input = np.array(test_data_input, dtype=float)
        print "Input data shape: " + str(test_data_input.shape)
        test_data_output = np.array(test_data_output, dtype=float)
        print "Output data shape: " + str(test_data_output.shape)
        difference_prediction = tf.reduce_mean(tf.sqrt(tf.square(y-y_)))
        print (sess.run(difference_prediction, feed_dict={x: test_data_input, y_: test_data_output}))

    @staticmethod
    def get_prediction(input_data):
        # Load the weights from the file, evaluate the output using numpy
        # Save the weights to a file
        model_weights = list()
        weights_file = open('pitcher_weights.csv', 'rb')
        spamreader = csv.reader(weights_file, delimiter=',')
        for weight in spamreader:
            model_weights.append(weight[0])
        weights_file.close()
        if len(input_data) != len(model_weights):
            return 0

        model_weight_array = np.array(model_weights, dtype=float)
        input_data_array = np.array(input_data, dtype=float)
        return np.matmul(model_weight_array, input_data_array)