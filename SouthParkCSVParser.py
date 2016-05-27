import csv,re,nltk
from nltk import *

def ParseCSV(filename):
    mainCharacters = {'Stan', 'Kyle', 'Cartman', 'Kenny', 'Butters', 'Wendy'
    , 'Jimmy','Garrison', 'Mackey'}


    f = open(filename, 'rt')
    try:
        reader = csv.reader(f)
        for row in reader:
            characters = re.split(',|/|and',row[2])
            #in case multiple character said the same line
            for character in characters:
                wfall = open("char_scripts/allChars.txt", 'a+')
                if character in mainCharacters:
                    wf = open("char_scripts/" + character +".txt", 'a+')
                    for sentence in sent_tokenize(row[3].strip('\n')):
                        if sentence[-1] == '\n':
                            wf.write(sentence + '\n')
                            wfall.write(character + '\t' + sentence+ '\n')
                        else:
                            wf.write(sentence +'\n')
                            wfall.write(character + '\t' + sentence +'\n')
                    wf.close()
                else:
                    for c in mainCharacters:
                        if c in character:
                            wf = open("char_scripts/" + c +".txt", 'a+')
                            for sentence in sent_tokenize(row[3].strip('\n')):
                                if sentence[-1] == '\n':
                                    wf.write(sentence + '\n')
                                    wfall.write(c + '\t' + sentence +'\n')
                                else:
                                    wf.write(sentence +'\n')
                                    wfall.write(c + '\t' + sentence +'\n')
                            wf.close()
                wfall.close()
    finally:
        f.close()

if __name__ == '__main__':
    ParseCSV('SouthParkData-master/All-seasons.csv')
