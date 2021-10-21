"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag).
"""
from typing import Counter
from collections import deque 

import math

def viterbi_3(train, test):
    laplace = 0.001
    wordset = set()
    tagset = set()
    for line in train:
        for word in line:
            wordset.add(word[0])
            tagset.add(word[1])

    
    
    
    initialtag = Counter()
    for line in train:
        initialtag[line[0][1]] += 1
    #initialtag_prob = dict[initialtag]
    #print(initialtag)
    initialtag_prob = {}

    for key in initialtag:
        initialtag_prob[key] = math.log((initialtag[key]+laplace)/(len(train)+laplace*len(initialtag)))
    initial_prob_unseen = math.log(laplace/(len(train)+len(initialtag)))

    print(initialtag_prob)
    print(initial_prob_unseen)
    print("len initial prob ", len(initialtag_prob))
    transition_prob, transition_prob_unseen = build_transition_dict(train,wordset,tagset,laplace)
    emission_prob, emission_prob_unseen = build_emission_dict(train,wordset,tagset,laplace)
    #print("transition prob")
    #print(transition_prob)
    #print("transition_prob_unseen")
    #print(transition_prob_unseen)
    #print("len transition prob ", len(transition_prob))
    #with open("dict2.txt", 'w') as f: 
    #    for key, value in transition_prob.items(): 
     #       f.write('%s:%s\n' % (key, value))
    #print("emission_prob prob")
    #print(emission_prob)
    #print("emission_prob")
    #print(emission_prob_unseen)
    #with open("dict4.txt", 'w') as f: 
    #    for key, value in emission_prob.items(): 
     #       f.write('%s:%s\n' % (key, value))

    print(inference(test[2],tagset,initialtag_prob,initial_prob_unseen,emission_prob,emission_prob_unseen, transition_prob, transition_prob_unseen))
    predict = []
    for line in test:
        predict.append(inference(line,tagset,initialtag_prob,initial_prob_unseen,emission_prob,emission_prob_unseen, transition_prob, transition_prob_unseen))

    return predict


def build_transition_dict(train,wordset,tagset,laplace):
    transition = Counter()
    transition_prob = {}
    transition_prob_unseen = math.log((laplace)/(len(train)+laplace*len(tagset)))
    #print(train[0])
    for line in train:
        for i in range(1,len(line)):
            curr = line[i][1]
            parent = line[i-1][1]
            transition[(parent,curr)]  += 1
    for tag1 in tagset:
        n = 0
        for tag2 in tagset:
            if (tag1, tag2) in transition:
                n += transition[(tag1,tag2)] # total number of known transition pairs with tag1
        for tag2 in tagset:
            if (tag1, tag2) in transition:
                transition_prob[(tag1, tag2) ] = math.log((transition[(tag1, tag2) ]+laplace)/(n+laplace*len(tagset)))
            else:
                transition_prob[(tag1, tag2) ] = transition_prob_unseen
    
    return transition_prob, transition_prob_unseen

    
def build_emission_dict(train,wordset,tagset,laplace):
    emission = Counter()
    emission_prob = {}
    count = Counter()
    emission_prob_unseen = math.log((laplace)/(len(train)+laplace*len(wordset)))
    for line in train:
        for word in line:
            emission[word] += 1
            count[word[1]] += 1
    for tag in tagset:
        for word in wordset:
            if (word,tag) in emission:
                emission_prob[(word,tag)] = math.log((emission[(word,tag)]+laplace)/(count[tag]+laplace*len(wordset)))
            else:
                emission_prob[(word,tag)]= emission_prob_unseen
    return emission_prob, emission_prob_unseen

def inference(line,tagset,initialtag_prob,initial_prob_unseen,emission_prob,emission_prob_unseen, transition_prob, transition_prob_unseen):
    #print("WORD length is", len(line))

    #matrix_prob = [{tag:0 for tag in tagset}] * len(line)
    #backward = [{tag:None for tag in tagset}]* len(line)
    matrix_prob = [{tag:0 for tag in tagset} for i in range(len(line))] #place holder for prob

    backward=[{tag:None for tag in tagset} for i in range(len(line))]#place holder for tag

  
    #find out initial tag prob
    for item in matrix_prob[0].items():
        if item[0] in initialtag_prob:
            p1 = initialtag_prob[item[0]]
        else:
            p1=initial_prob_unseen
        if (line[0], item[0]) in emission_prob:
            matrix_prob[0][item[0]] = p1 + emission_prob[(line[0], item[0])]
        else:
            matrix_prob[0][item[0]] = p1+ emission_prob_unseen

    #following trellis
    for i in range(1, len(matrix_prob)):
        for tag in matrix_prob[i].keys():
            max_p = -math.inf
            p1 = 0
            if (line[i],tag) in emission_prob:
                p1 = emission_prob[(line[i],tag)]
            else:
                p1 = emission_prob_unseen
            
            for tag1 in matrix_prob[i-1].keys(): # traceback for each possible way to current tag
                p2 =0
                if (tag1,tag ) in transition_prob:
                    p2 = transition_prob[(tag1,tag )]
                else:
                    p2 = transition_prob_unseen

                if p1+p2+matrix_prob[i-1][tag1] > max_p:
                    max_p = p1+p2+matrix_prob[i-1][tag1]
                    mostprobable_tag = tag1
            matrix_prob[i][tag] = max_p
            backward[i][tag] = mostprobable_tag
    n = len(line) -1
    result = deque()
    #result = ["END"]

    maxtag = max(matrix_prob[n], key=matrix_prob[n].get) #most probably last tag, start traceback
    #print("i",i,"maxtag", maxtag)
    #if i>100:
    #    print(backward)
    while n>=0 :
        result.appendleft((line[n],maxtag))
        maxtag = backward[n][maxtag]
        n -=1
    
    #print("tag length is", len(result))
    
    return result
            

