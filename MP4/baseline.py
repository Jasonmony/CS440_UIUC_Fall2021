"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""
import collections
from typing import Counter
def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
        test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
        E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    #print(train[0])
    print(test[0])

    word_tag_dict , tag_dict = build_dict(train)
    #print(word_tag_dict)
    predict_tag = []

    most_probable_tag_unseen = max(tag_dict,key = tag_dict.get)

    for line in test:
        predict_tag_this_line = []
        for word in line:
            if word in word_tag_dict:
                most_probable_tag = max(word_tag_dict[word],key = word_tag_dict[word].get)     
                predict_tag_this_line.append((word,most_probable_tag))
            else:
                predict_tag_this_line.append((word,most_probable_tag_unseen))
        predict_tag.append(predict_tag_this_line)
    
    print(predict_tag[0])


    return predict_tag


def build_dict(train): 
    sol_dict = {} # dictionary to store word and tag frequency
    count = Counter() # dictionary to store tag frequency
    for line in train:
        for word in line:
            if word[0] not in sol_dict:
                sol_dict[word[0]] = Counter()            
            sol_dict[word[0]][word[1]]  +=1 
            count[word[1]] +=1
            

    return sol_dict, count