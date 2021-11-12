# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
# Modified by Mahir Morshed for the spring 2021 semester
# Modified by Joao Marques (jmc12) for the fall 2021 semester 

"""
This is the main entry point for MP3. You should only modify code
within this file, neuralnet_learderboard and neuralnet_part2.py -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from utils import get_dataset_from_arrays
from torch.utils.data import DataLoader


class NeuralNet(nn.Module):
    def __init__(self, lrate, loss_fn, in_size, out_size):
        """
        Initializes the layers of your neural network.

        @param lrate: learning rate for the model
        @param loss_fn: A loss function defined as follows:
            @param yhat - an (N,out_size) Tensor
            @param y - an (N,) Tensor
            @return l(x,y) an () Tensor that is the mean loss
        @param in_size: input dimension
        @param out_size: output dimension

        For Part 1 the network should have the following architecture (in terms of hidden units):

        in_size -> 32 ->  out_size
        
        We recommend setting lrate to 0.01 for part 1.

        """
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        self.lrate = lrate 
        self.net = torch.nn.Sequential(torch.nn.Linear(in_size, 500),torch.nn.LeakyReLU(),  torch.nn.Linear(500, out_size))
        self.dropout = torch.nn.Dropout(0.1)

    

    def forward(self, x):
        """Performs a forward pass through your neural net (evaluates f(x)).

        @param x: an (N, in_size) Tensor
        @return y: an (N, out_size) Tensor of output from the network
        """
        x= self.dropout(x)
        x = self.net(x)
        #print(y.shape)
        return x
        #return torch.ones(x.shape[0], 1)

    def step(self, x,y):
        """
        Performs one gradient step through a batch of data x with labels y.

        @param x: an (N, in_size) Tensor
        @param y: an (N,) Tensor
        @return L: total empirical risk (mean of losses) for this batch as a float (scalar)
        """
        optimizer = optim.Adam(self.net.parameters(), lr=0.0001, weight_decay=1e-5)

        loss_fn = self.loss_fn
        loss_fn = loss_fn(self.forward(x),y)
        optimizer.zero_grad()
        loss_fn.backward()
        optimizer.step()
        loss = self.loss_fn(self.forward(x),y).detach().cpu().numpy()
        #print(loss)

        return loss


def fit(train_set,train_labels,dev_set,epochs,batch_size=100):
    """ Make NeuralNet object 'net' and use net.step() to train a neural net
    and net(x) to evaluate the neural net.

    @param train_set: an (N, in_size) Tensor
    @param train_labels: an (N,) Tensor
    @param dev_set: an (M,) Tensor
    @param epochs: an int, the number of epochs of training
    @param batch_size: size of each batch to train on. (default 100)

    This method _must_ work for arbitrary M and N.

    The model's performance could be sensitive to the choice of learning rate.
    We recommend trying different values in case your first choice does not seem to work well.

    @return losses: list of floats containing the total loss at the beginning and after each epoch.
            Ensure that len(losses) == epochs.
    @return yhats: an (M,) NumPy array of binary labels for dev_set
    @return net: a NeuralNet object
    """
    lrate = 2e-2
    loss_fn = torch.nn.CrossEntropyLoss()
    in_size = 3072
    out_size = 4
    net = NeuralNet(lrate, loss_fn, in_size, out_size)
    losses = []
    epochs = 1000
    train_set_norm = (train_set-train_set.mean())/(train_set.std())

    for i in range(epochs):

        features =  get_dataset_from_arrays(train_set_norm, train_labels)[i*batch_size%2250:(i+1)*batch_size%2250]['features']
        labels =  get_dataset_from_arrays(train_set_norm, train_labels)[i*batch_size%2250:(i+1)*batch_size%2250]['labels']

        losses.append(net.step(features, labels))
    yhats = []
    dev_set = (dev_set-train_set.mean())/(train_set.std())
    result = net(dev_set).detach().numpy()

    for i in range(len(result)):
        temp = int(np.argmax(result[i]))
        yhats.append(temp)
    yhats_array = np.array(yhats)
    return losses,yhats_array, net
