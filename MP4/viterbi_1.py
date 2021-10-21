"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag).
"""
from typing import Counter

import math

def viterbi_1(train, test):
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

    #matrix_prob = [{tag:0 for tag in tagset}] * len(line)
    #backward = [{tag:None for tag in tagset}]* len(line)
    matrix_prob = [{tag:0 for tag in tagset} for i in range(len(line))] #place holder for prob

    backward=[{tag:0 for tag in tagset} for i in range(len(line))]#place holder for tag

  
    #find out initial tag prob
    for item in tagset:
        if item in initialtag_prob:
            p1 = initialtag_prob[item]
        else:
            p1=initial_prob_unseen
        if (line[0], item) in emission_prob:
            matrix_prob[0][item] = p1 + emission_prob[(line[0], item)]
        else:
            matrix_prob[0][item] = p1+ emission_prob_unseen

    #following trellis
    for i in range(1, len(matrix_prob)):
        for tag in tagset:
            max_p = -math.inf
            if (line[i],tag) in emission_prob:
                p1 = emission_prob[(line[i],tag)]
            else:
                p1 = emission_prob_unseen
            
            for tag1 in tagset: # traceback for each possible way to current tag
                if (tag1,tag ) in transition_prob:
                    p2 = transition_prob[(tag1,tag )]
                else:
                    p2 = transition_prob_unseen

                if p1+p2+matrix_prob[i-1][tag1] > max_p:
                    max_p = p1+p2+matrix_prob[i-1][tag1]
                    mostprobable_tag = tag1
            matrix_prob[i][tag] = max_p
            backward[i][tag] = mostprobable_tag
    result = [(0,0)]*len(line) #place holder for result
    maxtag = max(matrix_prob[-1], key=matrix_prob[-1].get) #most probably last tag, start traceback
    #print("i",i,"maxtag", maxtag)
    #if i>100:
    #    print(backward)

    for i in range(len(line)-1):
        #print(i)
        result[len(line)-i-1] = (line[len(line)-i-1],maxtag)
        maxtag = backward[len(line)-i-1][maxtag]

    #print("tag length is", len(result))
    
    return result
            

