#!/usr/local/bin/python3

# TODO
# take in a character file
# analyze speech patterns (noun-verb-etc...)
# find useful key words used more often than others
# put in dictionary
# weigh the words for more biased sentence structures


import nltk
from nltk import *
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import random
import operator


meaninglessWords = {'the','a','an','i','you','her','him','his','and','to','with','we','is','are','be','will'}
cartman = {}
stan = {}
kyle = {}
wendy = {}
butters = {}
wn = WordNetLemmatizer()
def strip_non_alpha(s, compress=False):
	t = ""
	for c in s:
		if c.isalpha():
			t = t + c
		else:
			# if c == "'" or c == "/":
			# 	compress = True
			if compress==False:
				t = t + " "
		# compress = False
	return t

def normalize_statement(statement):
	'''
		Return a normalized version of d. This should be a list of
	    tokens that document_features can handle.
	'''
	statement = statement.lower()
	statement = strip_non_alpha(statement)
	statement = word_tokenize(statement)
	statement = [ wn.lemmatize(word) for word in statement]
	for word in statement:
		# having a list of meaningless words is better than pos tagging in this case bacause the script contains
		# little sentence structure causing the pos tagger to be less accurate
		if word in meaninglessWords:
			statement.remove(word)
    # statement = [wordnet_lemmatizer.lemmatize(word) for word in statement] + list(ngrams(statement,4))
	# print (statement)
	return ' '.join(statement)

def analyzeCharacter(character):
	'''
		open character file get their frequency distribution
	'''
	charfile = open("char_scripts/"+character+".txt", 'r')
	charfile2 = open("CharFreqDist/"+character+"FreqDist.txt", 'a+')
	ctr = 0
	fullText = ''
	try:
		lines = charfile.readlines()
		for line in lines:
			ctr += 1
			if ctr%100 == 0:
				print (ctr)
			fullText+=normalize_statement(line)+' '
		fd = FreqDist(word_tokenize(fullText))
		# print (list(fd))
		#tag the line, check if its possibly important before adding to dictionary
		# print (charWordDict)
		for key in fd:
			charfile2.write(key + '\t' + str(fd[key]) + '\n')
	finally:
		charfile.close()
		charfile2.close()


if __name__ == '__main__':
	analyzeCharacter('Cartman')
	analyzeCharacter('Stan')
	analyzeCharacter('Kyle')
	analyzeCharacter('Wendy')
	analyzeCharacter('Butters')

# Stan = {}
# Kyle = {}
# Cartman = {}
# Kenny = {}
# Butters = {}
# Wendy = {}
# Tweek_Tweak = {}
# Bebe = {}
# Bradley = {}
# Clyde = {}
# Craig = {}
# Dougie = {}
# Jimmy = {}
# Timmy = {}
# Token = {}
# Randy = {}
# Sharon = {}
# Shelly = {}
# Jimbo = {}
# Gerald = {}
# Shiela = {}
# Ike = {}
# Liane = {}
# Stuart = {}
# Carol = {}
# Stephen = {}
# Linda = {}
# Garrison = {}
# Mackey = {}
# Slave = {}
# Victoria = {}
# Barbrady = {}
# Big_Gay_Al = {}
# Ned = {}
# Hankey = {}
# Kim = {}
# Maxi = {}
# Mayor = {}
# Alphonse = {}
# Satan = {}
# Marvin = {}
# Terrence = {}
# Phillip = {}
# Harrison = {}
# Towelie = {}
# Chef = {}
# Pip_Pirrup = {}
# Choksondik = {}
# Crabtree = {}
