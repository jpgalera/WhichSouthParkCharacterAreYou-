#!/usr/local/bin/python3
import random,operator,os,sys,nltk,curses

from nltk import *
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from curses.ascii import isdigit
from nltk.corpus import cmudict

#####SETS OF VARIOUS IMPORTANT THINGS#####
mainCharacters = {'Stan', 'Kyle', 'Cartman', 'Kenny', 'Butters', 'Wendy'
    , 'Jimmy','Garrison', 'Mackey'}

verbList = {'agree','do','know','read','suggest','allow','eat','learn','remember',
'take','answer','explain','leave','run','talk','ask','fall','like','say','tell','be',
'feel','listen','see','think','become','fill','live','seem','travel','begin','find',
'look','sell','try','believe','finish','lose','send','turn','borrow','follow','make',
'set','understand','break','fly','may','shall','use','bring','forget','mean',
'should','wait','buy','get','meet','show','wake up','call','give','move','sit','walk',
'can','go','must','sleep','want','carry','happen','need','speak','watch','change',
'have','open','spend','will','close','hear','pay','stand','win','come','help','play',
'start','work','cut','hold','promise','stop','worry','decide','keep','put','study','write'}

conjunctionList = {'and','that','but','or','as','if','when','than','because','while','where',
'after','so','though','since','until','whether','before','although','nor','like','once','unless'
,'now','except'}

stopWords = set(stopwords.words('english'))

egocentricWordList = {'i','me','my'}
NonEgocentricWordList = {'we','us','our'}

###################################################

class Character:

    def __init__(self,name):
        '''
            characters' characteristics with numerical value
        '''
        if name in mainCharacters:
            self.folder = 'char_scripts/'
        else:
            self.folder = 'pres_scripts/raw'
        self.name = name
        self.charfile = open(self.folder + name + ".txt", 'r')
        self.speech = self.charfile.readlines()
        self.egocentrism = 0
        self.unformality = 0
        self.alliteration = 0
        self.anaphora = 0
        self.imperative = 0
        self.charfile.close()

    def is_Egocentric(self,tokenized_sentence):
        '''
            determines the egocentrism of a character
            based on how much they use peronal pronouns
        '''
        for word in egocentricWordList:
            if word.lower() in tokenized_sentence:
                self.egocentrism += 1
            if word in NonEgocentricWordList:
                self.egocentrism -= 1


    def is_Unformal(self, tokenized_sentence):
        '''
            determines the formality of character's speech.
            measured by how much contractions they use.
            more contractions => less formal
        '''
        for word in tokenized_sentence:
            if "'" in word and "'s" not in word:
                #distinguish between contractions and possessive
                self.unformality += 1

    def AALevel(self, tokenized_sentence):
        '''
            measures how frequent a character uses alliterations

            measures how frequent a character uses anaphora
        '''
        for i in range(len(tokenized_sentence)-1):
            if tokenized_sentence[i][0].lower() == tokenized_sentence[i+1][0].lower():
                if tokenized_sentence[i].lower() == tokenized_sentence[i+1].lower():
                    self.anaphora += 1
                else:
                    self.alliteration += 1

    def imperativeLevel(self,tokenized_sentence):
        '''
            analyze how imperative a character is
        '''
        bigrams = list(ngrams(tokenized_sentence,2))
        if bigrams.count(('have','to')) >= 1:
            self.imperative += 1
        for bigram in bigrams:
            if bigram[0] in verbList and bigram[1] in conjunctionList:
                self.imperative += 1

    def document_characteristics(self):
        '''
            document the character's level of egocentrism, formailty,
            alliteration and anaphora levels
        '''
        for line in self.speech:
            lineLower = line.lower()
            line_tokenized = word_tokenize(lineLower)
            self.is_Egocentric(line_tokenized)
            self.is_Unformal(line_tokenized)
            self.AALevel(line_tokenized)
            self.imperativeLevel(line_tokenized)



if __name__ == '__main__':
    charname = sys.argv[1]
    character = Character(charname)
    character.document_characteristics()
    print ("Character:" + character.name)
    print ('Egocentric Level: ' + str(round((character.egocentrism/len(character.speech)),4)))
    print ('Unformality Level: ' + str(round((character.unformality/len(character.speech)),4)))
    print ('Alliteration Level: ' + str(round((character.alliteration/len(character.speech)),4)))
    print ('Anaphora Level: ' + str(round((character.anaphora/len(character.speech)),4)))
    print ('Imperative Level: ' + str(round((character.imperative/len(character.speech)),4)))

    print('Comparing values with SouthPark characters')
    characterDict = {}
    f = open('AllCharAttributes.txt','r')
    lines = f.readlines()
    #we put more values in egocentrism,unformality and imperativeness rather than alliteration and anaphora
    for line in lines:
        char,ego,unformality,alliteration,anaphora,imperative = line.split('\t | \t')
        characterDict[char] = abs(3*(float(ego) -  round((character.egocentrism/len(character.speech)),4))) + abs(2*(float(unformality) - round((character.unformality/len(character.speech)),4))) + abs(float(alliteration) - round((character.alliteration/len(character.speech)),4)) + abs(float(anaphora) - round((character.anaphora/len(character.speech)),4)) + abs(2*(float(imperative) - round((character.imperative/len(character.speech)),4)))
    match = min(characterDict, key=characterDict.get)
    for key in sorted(characterDict, key=characterDict.get):
        print(key + ": " + str(characterDict[key]))
    print(charname + " matches " + match + ".")

    #image rendering
    from PIL import ImageTk
    import tkinter as tk

    root = tk.Tk()
    root.geometry("+{}+{}".format(100, 100))
    root.title("You have matched with " + match + '.')

    image1 = "images/"+ charname + ".png"
    image2 = "images/"+ match + ".png"

    photo1 = ImageTk.PhotoImage(file=image1)
    photo2 = ImageTk.PhotoImage(file=image2)

    tk.Label(root,image=photo1).grid(row=0, column=0)
    tk.Label(root,image=photo2).grid(row=0, column=1)


    root.mainloop()
