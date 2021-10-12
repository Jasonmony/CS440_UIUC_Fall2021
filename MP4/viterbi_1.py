"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag).
"""
from typing import Counter
import math

def viterbi_1(train, test):
    laplace = 0.001
    
    
    
    initialtag = Counter()
    for line in train:
        initialtag[line[-1][1]] += 1
    #initialtag_prob = dict[initialtag]
    print(initialtag)
    initialtag_prob = {}

    for key in initialtag:
        initialtag_prob[key] = math.log((initialtag[key]+laplace)/(len(train)+laplace*len(initialtag)))
    prob_unseen = math.log(laplace/(len(train)+len(initialtag)))


    transition_prob, transition_prob_unseen = build_transition_dict(train)



 


    return []


def build_transition_dict(train):
    transition = Counter()
    for line in train:
        for i in range(1,len(line)-1):
            curr = line[i][1]
            parent = line[i-1][1]
            transition[(parent,curr)]  += 1
    


