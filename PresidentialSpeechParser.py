import nltk,os,sys
from nltk import *


def Parse(charname):
    print("Parsing " + charname + "'s File...")
    s = ''
    f = open('pres_scripts/raw' + charname + '.txt','r')
    lines = f.readlines()
    for line in lines:
        s += line
    f.close()
    tokenized_s = sent_tokenize(s)
    fw = open('ParsedPresScripts/' + charname + '.txt.', 'w+')
    for sentence in tokenized_s:
        fw.write(sentence + '\n')
    fw.close()

if __name__ == '__main__':
    president = {'GeorgeBush', 'BarackObama', 'DonaldTrump'}
    for people in president:
        Parse(people)
