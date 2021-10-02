# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
from re import L
from warnings import filterwarnings
import numpy as np
import math
from tqdm import tqdm
from collections import Counter
import reader

"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


"""
  load_data calls the provided utility to load in the dataset.
  You can modify the default values for stemming and lowercase, to improve performance when
       we haven't passed in specific values for these parameters.
"""
 
def load_data(trainingdir, testdir, stemming=False, lowercase=False, silently=False):
    print(f"Stemming is {stemming}")
    print(f"Lowercase is {lowercase}")
    train_set, train_labels, dev_set, dev_labels = reader.load_dataset(trainingdir,testdir,stemming,lowercase,silently)
    return train_set, train_labels, dev_set, dev_labels



# Keep this in the provided template
def print_paramter_vals(laplace,pos_prior):
    print(f"Unigram Laplace {laplace}")
    print(f"Positive prior {pos_prior}")


"""
You can modify the default values for the Laplace smoothing parameter and the prior for the positive label.
Notice that we may pass in specific values for these parameters during our testing.
"""

def naiveBayes(train_set, train_labels, dev_set, laplace=0.01, pos_prior=0.75,silently=False):
    # Keep this in the provided template
    #laplace = 0.01
    #pos_prior = sum(train_labels)/len(train_labels)
    print_paramter_vals(laplace,pos_prior)
    pos_word_dict , neg_word_dict = build_word_dict(train_set, train_labels)
    pos_log_prob_dict, pos_unknown_log_prob = build_prob_dict(pos_word_dict,laplace)
    neg_log_prob_dict, neg_unknown_log_prob = build_prob_dict(neg_word_dict,laplace)
    print(len(dev_set))

    yhats = []
    for doc in tqdm(dev_set):
        #print(doc)
        pos = math.log(pos_prior)
        neg = math.log(1-pos_prior)
        
        for word in doc:
            if word in pos_word_dict:
                pos += pos_log_prob_dict[word]
            else:
                pos += pos_unknown_log_prob
            if word in neg_word_dict:
                neg += neg_log_prob_dict[word]
            else:
                neg += neg_unknown_log_prob
      

        yhats.append((pos > neg))
        #print(yhats)
    return yhats

 
# Keep this in the provided template
def print_paramter_vals_bigram(unigram_laplace,bigram_laplace,bigram_lambda,pos_prior):
    print(f"Unigram Laplace {unigram_laplace}")
    print(f"Bigram Laplace {bigram_laplace}")
    print(f"Bigram Lambda {bigram_lambda}")
    print(f"Positive prior {pos_prior}")


# main function for the bigrammixture model
def bigramBayes(train_set, train_labels, dev_set, unigram_laplace=0.01, bigram_laplace=0.003, bigram_lambda=0.4,pos_prior=0.5, silently=False):
    # Keep this in the provided template
    #unigram_laplace=0.01
    #bigram_laplace=0.003
    #bigram_lambda=0.4
    print_paramter_vals_bigram(unigram_laplace,bigram_laplace,bigram_lambda,pos_prior)
    pos_word_dict_bigram , neg_word_dict_bigram = build_word_dict_bigram(train_set, train_labels)
    pos_log_prob_dict_bigram, pos_unknown_log_prob_bigram = build_prob_dict(pos_word_dict_bigram,bigram_laplace)
    neg_log_prob_dict_bigram, neg_unknown_log_prob_bigram = build_prob_dict(neg_word_dict_bigram,bigram_laplace)
    #print(neg_log_prob_dict_bigram)

    pos_word_dict , neg_word_dict = build_word_dict(train_set, train_labels)
    pos_log_prob_dict, pos_unknown_log_prob = build_prob_dict(pos_word_dict,unigram_laplace)
    neg_log_prob_dict, neg_unknown_log_prob = build_prob_dict(neg_word_dict,unigram_laplace)

    #print("pos_unknown_log_prob_bigram",pos_unknown_log_prob_bigram)
    #print("neg_unknown_log_prob_bigram",neg_unknown_log_prob_bigram)
    #print("pos_unknown_log_prob",pos_unknown_log_prob)
    #print("neg_unknown_log_prob",neg_unknown_log_prob)
    yhats = []
    for doc in tqdm(dev_set,disable=silently):
        #print(doc)

        pos_uni = math.log(pos_prior)
        neg_uni = math.log(1-pos_prior)

        for word in doc:  # unigram
            if word in pos_word_dict:
                pos_uni += pos_log_prob_dict[word]
            else:
                pos_uni += pos_unknown_log_prob
            if word in neg_word_dict:
                neg_uni += neg_log_prob_dict[word]
            else:
                neg_uni += neg_unknown_log_prob

        pos_bi = math.log(pos_prior)
        neg_bi = math.log(1-pos_prior)
        for i in range(len(doc)-1): # bigram
            if (doc[i],doc[i+1]) in pos_word_dict_bigram:
                pos_bi += pos_log_prob_dict_bigram[(doc[i],doc[i+1])]
                #print("word in pos")
            else:
                pos_bi += pos_unknown_log_prob_bigram
                #print("word  not in pos")

            
            if (doc[i],doc[i+1]) in neg_word_dict_bigram:
                neg_bi += neg_log_prob_dict_bigram[(doc[i],doc[i+1])]
                #print("word in neg")

            else:
                neg_bi += neg_unknown_log_prob_bigram
                #print("word  not in neg")
        


        pos = bigram_lambda * pos_bi + (1-bigram_lambda) * pos_uni
        neg = bigram_lambda * neg_bi + (1-bigram_lambda) * neg_uni
        #print("pos is ", pos_bi)
        #print("neg is ", neg_bi)
        
        yhats.append((pos > neg))
    return yhats

def build_word_dict(training_set, training_label):
    worddict_pos = {}
    worddict_neg = {}

    for i in range(len(training_label)):
        sentence = training_set[i]
        if training_label[i] == 1:
            for word in sentence:
                if word in worddict_pos:
                    worddict_pos[word] +=1
                else:
                    worddict_pos[word] = 1
        else:
            for word in sentence:
                if word in worddict_neg:
                    worddict_neg[word] += 1
                else:
                    worddict_neg[word] = 1
    return worddict_pos, worddict_neg

def build_prob_dict(word_dict,laplace):
    log_probdict = {}
    number_of_words = 0
    number_of_different_words = len(word_dict)

    for word in word_dict:
         number_of_words += word_dict[word]
    
    unknown_prob = laplace/(number_of_words + laplace*(number_of_different_words +1))

    for word in word_dict:
        log_prob = math.log(word_dict[word]*unknown_prob/laplace + unknown_prob)
        log_probdict[word] = log_prob
    
    return log_probdict, math.log(unknown_prob)

def build_word_dict_bigram(training_set, training_label):
    worddict_pos = {}
    worddict_neg = {}
    if len(training_set) < 5:
        print(training_set)
    if len(training_label) < 5:
        print(training_label)    
    for i in range(len(training_label)):
        sentence = training_set[i]
        #print(len(sentence))
        #n+= len(sentence)
        if training_label[i] == 1:
            for j in range(len(sentence)-1):
                if (sentence[j],sentence[j+1]) in worddict_pos:
                    worddict_pos[(sentence[j],sentence[j+1])] +=1
                else:
                    worddict_pos[(sentence[j],sentence[j+1])] = 1
        else:
            for j in range(len(sentence)-1):
                if (sentence[j],sentence[j+1]) in worddict_neg:
                    worddict_neg[(sentence[j],sentence[j+1])] += 1
                else:
                    worddict_neg[(sentence[j],sentence[j+1])] = 1
    if len(worddict_pos)<5:
        print (worddict_pos)
    if len(worddict_neg)<5:
        print (worddict_neg)
    return worddict_pos, worddict_neg
