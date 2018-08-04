import tensorflow as tf
import numpy as np
from math import ceil
from tfrbm import BBRBM, GBRBM
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib import rnn
import word2vecCNN

with tf.device('/gpu:0'):
    tf.reset_default_graph()
    tf.set_random_seed(1)
    np.random.seed(1)

    # Hyper Parameters
    BATCH_SIZE = 64
    TIME_STEP = 10          # rnn time step / image height
    INPUT_SIZE = 64         # rnn input size / image width
    LR = 0.01               # learning rate

    # data
    abnormal_code = "11"
    train_data_list,label_list = word2vecCNN.embedding_data(abnormal_code)
    train_x = np.reshape(train_data_list,(len(train_data_list),-1))[:10]
    train_y = np.array(label_list)[:10]
    print ("train_data_list.shape" ,train_x.shape)
    print ("label_list.shape" ,train_y.shape)
    test_x = train_x[7:]
    test_y = train_y[7:]

    print ("test_data_list.shape" ,test_x.shape)
    print ("label_list.shape" ,test_y.shape)


    # RBM
    bbrbm = BBRBM(n_visible=train_x.shape[1], n_hidden=640, learning_rate=0.01, momentum=0.95, use_tqdm=True)
    errs = bbrbm.fit(train_x, n_epoches=2, batch_size=10)
    doc_vec = bbrbm.transform(train_x.reshape(train_x.shape[0],-1))
    # doc_vec = doc_vec.reshape(train_data_list.shape[0],10,-1)
    print ("doc_vec.shape", doc_vec.shape)



    # tensorflow placeholders
    tf_x = tf.placeholder(tf.float32, [None, TIME_STEP * INPUT_SIZE])       # shape(batch, 640)
    image = tf.reshape(tf_x, [-1, TIME_STEP, INPUT_SIZE])                   # (batch, height, width, channel)
    tf_y = tf.placeholder(tf.int32, [None, 2])                             # input y


    # RNN
    lstm_cell = tf.contrib.rnn.BasicLSTMCell(num_units=32)
    #lstm_cell = tf.contrib.rnn.DropoutWrapper(cell=lstm_cell, output_keep_prob=0.75)   # Dropout层
    outputs, (h_c, h_n) = tf.nn.dynamic_rnn(
        lstm_cell,                   # cell you have chosen
        image,                      # input
        initial_state=None,         # the initial hidden state
        dtype=tf.float32,           # must given if set initial_state = None
        time_major=False,           # False: (batch, time step, input); True: (time step, batch, input)
    )
    output = tf.layers.dense(outputs[:, -1, :], 2)              # output based on the last output step

    loss = tf.losses.softmax_cross_entropy(onehot_labels=tf_y, logits=output)           # compute cost
    train_op = tf.train.AdamOptimizer(LR).minimize(loss)

    accuracy = tf.metrics.accuracy(          # return (acc, update_op), and create 2 local variables
        labels=tf.argmax(tf_y, axis=1), predictions=tf.argmax(output, axis=1),)[1]

    sess = tf.Session()
    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer()) # the local var is for accuracy_op
    sess.run(init_op)     # initialize var in graph


    BATCH_NUM = ceil(len(train_x)/BATCH_SIZE)
    for i in range(12):    # training  重复训练10000次
        step = 0
        start = 0
        end = start + BATCH_SIZE
        print ("Epoch: " + str(i+1) + 100*".")
        for step in range(BATCH_NUM):   # 对每个Batch进行训练
            _, loss_ = sess.run([train_op, loss], feed_dict = {tf_x: doc_vec[start:end], tf_y: train_y[start:end]})
            start = start + BATCH_SIZE
            end = start + BATCH_SIZE
        accuracy_ = sess.run(accuracy, {tf_x: test_x, tf_y: test_y})     # testing
        print('train loss: %.4f' % loss_, '| test accuracy: %.2f' % accuracy_)