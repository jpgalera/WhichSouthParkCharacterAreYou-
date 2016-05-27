#!/usr/local/bin/python3
from classifier import *
'''
    Only run this file once to generate data of all the characters that were analyzed.
'''
mainCharacters = {'Stan', 'Kyle', 'Cartman', 'Kenny', 'Butters', 'Wendy'
    , 'Jimmy','Garrison', 'Mackey'}

def getAllCharacterAttributes():
    f = open('AllCharAttributes.txt','w+')
    for character in mainCharacters:
        char = Character(character)
        char.document_characteristics()
        f.write( char.name + '\t | \t'
        # written to file in the following order:
        # character name, egocentrism,unformality,alliterationLevel,anaphoraLevel,imperativeLevel
        + str(round((char.egocentrism/len(char.speech)),4)) + '\t | \t'
        + str(round((char.unformality/len(char.speech)),4)) + '\t | \t'
        + str(round((char.alliteration/len(char.speech)),4)) + '\t | \t'
        + str(round((char.anaphora/len(char.speech)),4)) + '\t | \t'
        + str(round((char.imperative/len(char.speech)),4)) + '\n')

if __name__ == '__main__':
    getAllCharacterAttributes()
