#!/usr/bin/python3

import nltk
from nltk import *
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import random


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


def strip_non_alpha(s, compress=False):
	t = ""
	for c in s:
		if c.isalpha():
			t = t + c
		else:
			if compress==False:
				t = t + " "
	return t

wordnet_lemmatizer = WordNetLemmatizer()

def normalize_statement(d):
	'''
	Return a normalized version of d. This should be a list of
	tokens that document_features can handle.
	'''
	d = d.lower()
	d = strip_non_alpha(d)
	d = word_tokenize(d)
	return d


def document_features(d, train_features):
	''' implement a 'bag of features' '''

	setd = set(d)
	bigrams = list(ngrams(d,2))
	features = {}
	a = ['i','me','my','we','us','our','ours']
	for x in train_features:
		features['contains({})'.format(x)] = (x in setd)
	for x in d:
		features['is_informal({})'.format(x)] = "'" in x and "'s" not in x
	for x,y in bigrams:
		features['anaphora({})'.format((x,y))] = (x == y)
		features['alliteration({})'.format((x,y))] = (x[0] == y[0])
		features['imperative({})'.format((x,y))] = (x,y) == ('have','to')
		features['imperative({})'.format((x,y))] = x in verbList and y in conjunctionList
	return features

def load_data(filename):
	count = 0
	data = []
	f = open(filename, "r")
	for line in f:
		count += 1
		if count%100 == 0:
			print(count)
		line = line.strip()
		if '\t' in line:
			[classification, statement]  = line.split("\t")
			ns = normalize_statement(statement)
			data.append((ns, classification))
	f.close()
	return data

print("Loading training data")
data = load_data("char_scripts/allChars.txt")
train_data = data[:int(len(data)*0.75)]
print("Figuring out the features")
all_features = []
for (ns, classification) in train_data:
	all_features.extend(ns)

train_freq = FreqDist(all_features)
train_features = [ x for (x, count) in train_freq.most_common(200)]# 2000 most common features
print(train_features)

print("Computing the training set")
# Q6: Explain the difference between train_features and train_set
train_set = [ (document_features(ns, train_features), classification) for (ns, classification) in train_data ]

print("Building the NaieveBayes classifier")
classifier = nltk.NaiveBayesClassifier.train(train_set)
classifier.show_most_informative_features(50)

print("Testing the classifier")
test_data = data[int(len(data)*0.75):]
test_set = [ (document_features(ns, train_features), classification) for (ns, classification) in test_data ]
print(nltk.classify.accuracy(classifier, test_set))

'''
# In case you wanted to look at another classifier...
print("DecisionTree")
classifier = nltk.DecisionTreeClassifier.train(train_set)
sorted(classifier.labels())
print(classifier)
print(nltk.classify.accuracy(classifier, test_set))
'''

while True:
	statement = input("give me a statement:")
	ns = normalize_statement(statement)
	features = document_features(ns, train_features)
	# print(features)
	print(classifier.classify(features))
