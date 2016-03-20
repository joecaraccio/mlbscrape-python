
import tensorflow as tf
import numpy as np
from mlb_database import MlbDatabase
from hitter_game_entry import HitterGameEntry
import random

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

# Get a random sample from the database query
def get_stochastic_batch(db_query, num_samples):
    playerSamples = random.sample([itm for itm in db_query], num_samples)
    x = list()
    y = list()
    for item in playerSamples:
        inputVector = item.to_input_vector()
        if inputVector is not None:
            x.append(inputVector)
            """if item.career_ab == 0:
                x.append([0.0])
            else:
                #print float(item.career_h) / float(item.career_ab)
                x.append([float(item.career_h) / float(item.career_ab)])
            """
            y.append([item.draft_kings_points])
            
    assert len(x) == num_samples
    return x, y
    
mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()

db_query = databaseSession.query(HitterGameEntry)
mlb_training_data, mlb_evaluation_data = get_train_eval_data(db_query, 0.8)

#TODO: use tensorflow to build a deep neural network
#TODO: the first example will be just career BA

# 63 stat inputs, any arbitrary number of players (100 x 63)
x = tf.placeholder(tf.float32, [None, 64])

# 63 x 10 weights
w = tf.Variable(tf.zeros([64, 1]))

# 10 element bias vector
b = tf.Variable(tf.zeros([1, 64]))
#b = tf.Variable(tf.float32, [None, 1])

# Network theoretical output
# 10 x 1
y = tf.reduce_sum(tf.matmul(x, w) + b, 1)

# The true output is just the DraftKings points
# Player actual instances x 1
y_ = tf.placeholder(tf.float32, [None, 1])

# The cross entropy of the output as compared to the true output
#cross_entropy = y_*tf.log(y)
# Minimize the square error
square_error = tf.square(y_ - y)

# Each training iteration will be conducted using gradient descent by minimizing the cross entropy
#train_step=tf.train.GradientDescentOptimizer(0.00000000000000000000001).minimize(cross_entropy)
train_step = tf.train.AdamOptimizer(0.0001).minimize(square_error)

# Initialize all TensorFlow variables
init = tf.initialize_all_variables()

sess = tf.Session()

sess.run(init)
# Perform the actual training of the net
# Stochastic training with 100 instances run 1000 times
for i in range(100000):
    batch_xs, batch_ys = get_stochastic_batch(mlb_training_data, 100)
    batch_xs = np.array(batch_xs, dtype=float)
    batch_ys = np.array(batch_ys, dtype=float)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
    w.eval(sess)
    
w.eval(sess)

test_data_input = list()
test_data_output = list()
for data in mlb_evaluation_data:
    test_data_input.append(data.to_input_vector())
    test_data_output.append([data.draft_kings_points])
test_data_input = np.array(test_data_input, dtype=float)
test_data_output = np.array(test_data_output, dtype=float)
difference_prediction = y-y_
difference_length = y-y_
print (sess.run(difference_prediction, feed_dict={x: test_data_input, y_: test_data_output}))