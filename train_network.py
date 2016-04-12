
import tensorflow as tf
import numpy as np
from mlb_database import MlbDatabase
from hitter_game_entry import HitterGameEntry
import random


#TODO: add the 2 hitters right before the hitter of interest in the batting order

def get_batting_order_offset(order_number, offset_value):
    batting_position = order_number + offset_value
    if order_number > 9:
        return 1
    elif order_number < 1:
        return 9
    else:
        return batting_position

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
def get_stochastic_batch(db_query, db_session, num_samples):
    playerSamples = random.sample([itm for itm in db_query], num_samples)
    x = list()
    y = list()
    for item in playerSamples:
        inputVector = item.to_input_vector()
        #if inputVector is not None:
            #x.append(inputVector)
            #y.append([item.draft_kings_points])
        try:
            previous_hitter = db_session.query(HitterGameEntry).filter(HitterGameEntry.team == item.team,
                                                                       HitterGameEntry.game_id == item.game_id,
                                                                       HitterGameEntry.batting_order == str(get_batting_order_offset(int(item.batting_order), -1 )))
            inputVector += previous_hitter[0].to_input_vector()
            next_previous_hitter = db_session.query(HitterGameEntry).filter(HitterGameEntry.team == item.team,
                                                                       HitterGameEntry.game_id == item.game_id,
                                                                       HitterGameEntry.batting_order == str(get_batting_order_offset(int(item.batting_order), -2 )))
            inputVector += next_previous_hitter[0].to_input_vector()
            on_deck_hitter = db_session.query(HitterGameEntry).filter(HitterGameEntry.team == item.team,
                                                                       HitterGameEntry.game_id == item.game_id,
                                                                       HitterGameEntry.batting_order == str(get_batting_order_offset(int(item.batting_order), 1 )))
            inputVector += on_deck_hitter[0].to_input_vector()
            in_hole_hitter = db_session.query(HitterGameEntry).filter(HitterGameEntry.team == item.team,
                                                                       HitterGameEntry.game_id == item.game_id,
                                                                       HitterGameEntry.batting_order == str(get_batting_order_offset(int(item.batting_order), 2 )))
            inputVector += in_hole_hitter[0].to_input_vector()
            x.append(inputVector)
            y.append([item.draft_kings_points])
        except:
            #print "Could not find the hitters in the database. Omitting these hitters."
            continue

    #assert len(x) == num_samples
    return x, y
    
mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()

db_query = databaseSession.query(HitterGameEntry)
mlb_training_data, mlb_evaluation_data = get_train_eval_data(db_query, 0.8)

# 63 stat inputs, any arbitrary number of players (100 x 63)
x = tf.placeholder(tf.float32, [None, 52*5])

# 63 x 10 weights
w = tf.Variable(tf.zeros([52*5, 1]))

# 10 element bias vector
b = tf.Variable(tf.zeros([1, 52*5]))
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
for i in range(300):
    batch_xs, batch_ys = get_stochastic_batch(mlb_training_data, databaseSession, 250)
    batch_xs = np.array(batch_xs, dtype=float)
    batch_ys = np.array(batch_ys, dtype=float)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
    print "Iteration %i" % i
    
w.eval(sess)

test_data_input = list()
test_data_output = list()
for data in mlb_evaluation_data:
    try:
        inputVector = data.to_input_vector()
        previous_hitter = databaseSession.query(HitterGameEntry).filter(HitterGameEntry.team == data.team,
                                                                   HitterGameEntry.game_id == data.game_id,
                                                                   HitterGameEntry.batting_order == str(get_batting_order_offset(int(data.batting_order), -1 )))
        inputVector += previous_hitter[0].to_input_vector()
        next_previous_hitter = databaseSession.query(HitterGameEntry).filter(HitterGameEntry.team == data.team,
                                                                   HitterGameEntry.game_id == data.game_id,
                                                                   HitterGameEntry.batting_order == str(get_batting_order_offset(int(data.batting_order), -2 )))
        inputVector += next_previous_hitter[0].to_input_vector()
        on_deck_hitter = databaseSession.query(HitterGameEntry).filter(HitterGameEntry.team == data.team,
                                                                   HitterGameEntry.game_id == data.game_id,
                                                                   HitterGameEntry.batting_order == str(get_batting_order_offset(int(data.batting_order), 1 )))
        inputVector += on_deck_hitter[0].to_input_vector()
        in_hole_hitter = databaseSession.query(HitterGameEntry).filter(HitterGameEntry.team == data.team,
                                                                   HitterGameEntry.game_id == data.game_id,
                                                                   HitterGameEntry.batting_order == str(get_batting_order_offset(int(data.batting_order), 2 )))
        inputVector += in_hole_hitter[0].to_input_vector()
        test_data_input.append(inputVector)
        test_data_output.append([data.draft_kings_points])
    except:
        print "Could not find the hitters in the database. Omitting these hitters."
        continue
test_data_input = np.array(test_data_input, dtype=float)
print "Input data shape: " + str(test_data_input.shape)
test_data_output = np.array(test_data_output, dtype=float)
print "Output data shape: " + str(test_data_output.shape)
difference_prediction = tf.reduce_mean(tf.sqrt(tf.square(y-y_)))
print (sess.run(difference_prediction, feed_dict={x: test_data_input, y_: test_data_output}))