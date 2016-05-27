#!/usr/local/bin/python3

import random, sys, nltk
from nltk import *

######USED for chain building######
sentenceStarters = []
chainDictOptions = {} #dictionary of dictionaries containing current chain and possible next words
chainDict = {} # dictionary for current chain

def getWords(filename):
    global sentenceStarters
    f = open(filename, 'r')
    lines = f.readlines()
    wordsList = []
    for line in lines:
        tokenized_line = word_tokenize(line)
        wordsList +=  tokenized_line
        # Get the first word of every sentence to use as sentence starters
        if tokenized_line[0] not in '.,?!':
            sentenceStarters.append(tokenized_line[0])
    return wordsList

def chainBuilding(wordList, chainLength):
    global chainDictOptions
    for i in range(len(wordList)-1):
        if i <= chainLength:
            prev = wordList[:i + 1]
        else:# index is past the chainLength
            prev = wordList[i - chainLength + 1 :i + 1]
        nextWord = wordList[i + 1]
        chainMapping(prev,nextWord)
    for new_prev, possibleNextWords in chainDictOptions.items():
        total = sum(possibleNextWords.values())
        chainDict[new_prev] = {key:value/total for key,value in possibleNextWords.items()}

def chainMapping(prev,nextWord):
    global chainDictOptions
    new_prev = tuple(prev)
    while prev!=[]:
        if new_prev in chainDictOptions:
            if nextWord in chainDictOptions[new_prev]:
                chainDictOptions[new_prev][nextWord] += 1
            else:
                chainDictOptions[new_prev][nextWord] = 1
        else:
            chainDictOptions[new_prev] = {}
            chainDictOptions[new_prev][nextWord] = 1
        prev = prev[1:]
        new_prev = tuple(prev)


def next(prev):
    ret = ''
    choice = random.random()
    total = 0
    while tuple(prev) not in chainDict:
        prev = prev[1:]
    for key,value in chainDict[tuple(prev)].items():
        total += value
        if total >= choice and ret =='':
            ret = key
    return ret


def genSentence(chainLength):
    # First pick a word to start the sentence
    curr = random.choice(sentenceStarters)
    sentence = curr.capitalize()# current form of sentence is capitalized version of the first word
    prev = [curr]
    while curr != '.':
        curr = next(prev)
        prev.append(curr)
        if (curr not in ".,!?;"):
            sentence += " "
        sentence += curr
        if len(prev) > chainLength:
            prev = prev[1:]
    return sentence


if __name__ == "__main__":
    if len(sys.argv) < 1:
        sys.stderr.write('Usage: ' + sys.argv [0] + 'characterName=All (First letter capitalized) chainLength=1\n')
        sys.exit(1)

    mainCharacters = {'Stan', 'Kyle', 'Cartman', 'Kenny', 'Butters', 'Wendy'
        , 'Jimmy','Garrison', 'Mackey'}
    charname='All'
    chainLength=1
    if len(sys.argv) == 2:
        charname = sys.argv[1]
    if len(sys.argv) == 3:
        charname = sys.argv[1]
        chainLength = int(sys.argv[2])

    if charname == 'All':
        for character in mainCharacters:
            fchar = open('generatedscripts/generated'+character+".txt",'w+')
            print(character)
            for i in range(1,6):
                #generate 1000 sentences using chain of size i and write it to file
                ctr = 0
                chainBuilding(getWords("char_scripts/"+character+".txt"), i)
                while ctr < 1000:
                    fchar.write(genSentence(i)+'\n')
                    if ctr%100 == 0:
                        print (ctr)
                    ctr += 1
    else:
        chainBuilding(getWords("char_scripts/"+charname+".txt"), chainLength)
        print (genSentence(chainLength))
