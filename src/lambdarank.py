#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2017 Wan Li. All Rights Reserved
#
########################################################################

"""
File: lambdarank.py
Author: Wan Li
Date: 2017/11/27 10:41:01
"""

import tensorflow as tf
import config

weights = {
        "hidden": tf.Variable(tf.random_normal(
            [config.FEATURE_NUM, config.LAYER_WIDTH]), name="W_hidden"),
        "out": tf.Variable(tf.random_normal([config.LAYER_WIDTH, 1]), name="W_out"),
        "linear": tf.Variable(tf.random_normal([config.FEATURE_NUM, 1]), name="W_linear")
}

biases = {
        "hidden": tf.Variable(tf.random_normal([config.LAYER_WIDTH]), name="b_hidden"),
        "out": tf.Variable(tf.random_normal([1]), name="b_out"),
        "linear": tf.Variable(tf.random_normal([1]), name="b_linear"),
}

with tf.name_scope("mlp"):
    with tf.name_scope("input"):
        X = tf.placeholder(tf.float32, [None, config.FEATURE_NUM], name="X")
        Y = tf.placeholder(tf.float32, [None, 1], name="Y")
    if config.USE_HIDDEN_LAYER == True:
        with tf.name_scope("hidden_layer"):
            layer_h1 = tf.add(tf.matmul(X, weights["hidden"]), biases["hidden"])
            layer_h1 = tf.nn.relu(layer_h1)
        with tf.name_scope("out_layer"):
            y = tf.add(tf.matmul(layer_h1, weights["out"]), biases["out"])
    else:
        with tf.name_scope("linear_layer"):
            y = tf.add(tf.matmul(X, weights["linear"]), biases["linear"])

with tf.name_scope("matrices"):
    # score diff matrix with shape [doc_count, doc_count]
    sigma_ij = y - tf.transpose(y)
    # label diff matrix with shape [doc_count, doc_count]
    Sij_ = Y - tf.transpose(Y)
    Sij = tf.minimum(1.0, tf.maximum(-1.0, Sij_))

    loss = tf.reduce_sum(y) # temp

with tf.name_scope("train_op"):
    train_op = tf.train.GradientDescentOptimizer(config.LEARNING_RATE).minimize(loss)
