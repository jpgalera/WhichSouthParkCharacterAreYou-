#!/usr/local/bin/python3
import random,operator,os,sys,nltk

from nltk import *
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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

stopWords = {words.strip() for words in open('StopWords2','r').readlines()}

egocentricWordList = {'i','me','my'}
NonEgocentricWordList = {'we','us','our'}

###################################################
######HELPER FUNCTION FOR COUNTING SYLLABLES#######



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
        self.affirmative = 0
        self.negative = 0
        self.interrogative = 0
        self.buzzwords = set({})#set of non-stop words the character uses
        self.charfile.close()

    def is_Egocentric(self,tokenized_sentence):
        '''
            determines the egocentrism of a character
            based on how much they use peronal pronouns
        '''
        for word in egocentricWordList:
            if word.lower() in tokenized_sentence:
                self.egocentrism += 1
        for word in NonEgocentricWordList:
            if word.lower() in tokenized_sentence:
                self.egocentrism -= 1


    def is_Unformal(self, sentence):
        '''
            determines the formality of character's speech.
            measured by how much contractions they use.
            more contractions => less formal
        '''
        if "'" in sentence and "'s" not in sentence:
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

    def interrogativeLevel(self, sentence):
        '''
            analyze how often a character asks a question
        '''
        if '?' in sentence:
            self.interrogative += 1

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
                break

    def buzzwordsUse(self, tokenized_sentence):
        '''
            Calculates how dense a character uses non-stopwords
        '''
        for word in tokenized_sentence:
            if word.lower() not in stopWords:
                self.buzzwords.add(word.lower())

    def affirmativityLevel(self, tokenized_sentence):
        '''
            How  often do the characters talk in an affirmative manner?
        '''
        for word in tokenized_sentence:
            if word.lower()[:3] == "yes" or word.lower()[:3] == "yea" or word.lower()[:3] == "yup":
                self.affirmative += 1
                break


    def negativityLevel(self,tokenized_sentence):
        '''
            How often does the character disgaree with something
        '''
        for word in tokenized_sentence:
            if word.lower()[:2] == "no":
                self.negative += 1
                break

    def document_characteristics(self):
        '''
            document the character's level of egocentrism, formailty,
            alliteration and anaphora levels
        '''
        for line in self.speech:
            lineLower = line.lower()
            line_tokenized = word_tokenize(lineLower)
            self.is_Egocentric(line_tokenized)
            self.is_Unformal(lineLower)
            self.AALevel(line_tokenized)
            self.imperativeLevel(line_tokenized)
            self.buzzwordsUse(line_tokenized)
            self.affirmativityLevel(line_tokenized)
            self.negativityLevel(line_tokenized)
            self.interrogativeLevel(lineLower)



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
    f = open('AllGeneratedCharAttributes.txt','r')
    lines = f.readlines()
    for line in lines:
        char,interrogative, buzz, affirmative, negative, ego,unformality,alliteration,anaphora,imperative = line.split('\t | \t')
        characterDict[char] = (2*(float(ego)+round((character.egocentrism/len(character.speech)),4)))+ abs(1.5*(float(unformality) - round((character.unformality/len(character.speech)),4)))+ abs(float(alliteration)-round((character.alliteration/len(character.speech)),4))+ abs(float(anaphora)-round((character.anaphora/len(character.speech)),4))+ abs(2*(float(imperative)-round((character.imperative/len(character.speech)),4)))+ abs(2*(float(interrogative)-round((character.interrogative/len(character.speech)),4)))+ abs(1.5*(float(affirmative)-round((character.affirmative/len(character.speech)),4)))+ abs(1.5*(float(negative)-round((character.negative/len(character.speech)),4)))+ abs(float(buzz)-round((len(character.buzzwords)/len(character.speech)),4))

    match = min(characterDict, key=characterDict.get)
    for key in sorted(characterDict, key=characterDict.get):
        print(key + ": " + str(characterDict[key]))
    print(charname + " matches " + match + ".")
    print("Congratulations....You have just voted for " + match + '.')

    #image rendering
    # from PIL import ImageTk
    # try:
    #     # Python2
    #     import Tkinter as tk
    # except ImportError:
    #     # Python3
    #     import tkinter as tk

    # root = tk.Tk()
    # root.geometry("+{}+{}".format(100, 100))
    # root.title("You have matched with " + match + '.')

    # # pick image files you have in your working directory
    # # or use full path
    # # PIL's ImageTk allows .gif  .jpg  .png  .bmp formats
    # image1 = "images/"+ charname + ".png"
    # image2 = "images/"+ match + ".png"

    # # PIL's ImageTk converts to an image object that Tkinter can handle
    # photo1 = ImageTk.PhotoImage(file=image1)
    # photo2 = ImageTk.PhotoImage(file=image2)

    # # put the image objects on labels in a grid layout
    # tk.Label(root,image=photo1).grid(row=0, column=0)
    # tk.Label(root,image=photo2).grid(row=0, column=1)

    # # execute the event loop
    # root.mainloop()
