# mp4.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created Fall 2018: Margaret Fleck, Renxuan Wang, Tiantian Fang, Edward Huang (adapted from a U. Penn assignment)
# Modified Spring 2020: Jialu Li, Guannan Guo, and Kiran Ramnath
# Modified Fall 2020: Amnon Attali, Jatin Arora
# Modified Spring 2021 by Kiran Ramnath (kiranr2@illinois.edu)

"""
This file should not be submitted - it is only meant to test your implementation of the Viterbi algorithm. 

See Piazza post @650 - This example is intended to show you that even though P("back" | RB) > P("back" | VB), 
the Viterbi algorithm correctly assigns the tag as VB in this context based on the entire sequence. 
"""
from utils import read_files, get_nested_dictionaries
import math
from typing import Counter

def main():
    test, emission, transition, output = read_files()
    emission, transition = get_nested_dictionaries(emission, transition)
    initial = transition["START"]
    #print(transition)
    #print(initial)
    #print(emission)
    print(test[0])

    prediction = []
    
    """WRITE YOUR VITERBI IMPLEMENTATION HERE"""
    backward = []
    for line in test:
        initialtag = max(initial, key=initial.get) 
        initialprob = emission[initialtag][line[0]]
        backward.append(initial[initialtag]*initialprob)

        for i in range(1, len(line)):
            for tag in transition.keys():
                max_p = -math.inf
                mostprobable_tag = None
                p1 = 0               
                p1 = emission[tag][line[i]]                
                for tag1 in transition.keys():
                    p2 =0
                    p2 = transition[tag1][tag]                  

                    if p1*p2*transition[i-1][tag1] > max_p:
                        max_p = p1*p2*backward[i-1][tag1]
                        mostprobable_tag = tag1
                matrix_prob[i][tag] = max_p
                backward[i][tag] = mostprobable_tag
    index = len(matrix_prob) -1


        
    print('Your Output is:',prediction,'\n Expected Output is:',output)

def make_matrix(sentence, tags):
    #matrix = [{tag:0 for tag in tags} for i in range(len(sentence))]
    matrix = []
    for i in range(len(sentence)): 
        matrix.append({tag:0 for tag in tags})
    return matrix

def make_b_ptr(sentence, tags):
    back_ptr=[]
    for i in range(len(sentence)):
        back_ptr.append({tag:None for tag in list(tags)})
    return back_ptr

def inference(line,tagset,initialtag_prob,initial_prob_unseen,emission_prob,emission_prob_unseen, transition_prob, transition_prob_unseen):
    #print("WORD length is", len(line))

    matrix_prob = [{tag:0 for tag in tagset}] * len(line)
    backward = [{tag:None for tag in tagset}]* len(line)
    #find out initial tag prob
    probinitial = 0
    for tag, prob in matrix_prob[0].items():
        if tag in initialtag_prob:
            probinitial = initialtag_prob[tag]
        else:
            probinitial = initial_prob_unseen
        if (line[1],tag) in emission_prob:
            probinitial += emission_prob[(line[1],tag)]
        else:
            probinitial += emission_prob_unseen
        matrix_prob[0][tag] = probinitial
    
    #following tag
    for i in range(1, len(matrix_prob)):
        for tag in matrix_prob[i].keys():
            max_p = -math.inf
            mostprobable_tag = None
            p1 = 0
            if (line[i],tag) in emission_prob:
                p1 = emission_prob[(line[i],tag)]
            else:
                p1 = emission_prob_unseen
            
            for tag1 in matrix_prob[i-1].keys():
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
    index = len(matrix_prob) -1
    result = []
    #result = ["END"]

    maxtag = max(matrix_prob[index], key=lambda key:matrix_prob[index][key])
    while maxtag != None and index >= 0:
        result = [(line[index],maxtag)] + result
        maxtag = backward[index][maxtag]
        index -=1
    
    #print("tag length is", len(result))
    
    return result

if __name__=="__main__":
    main()