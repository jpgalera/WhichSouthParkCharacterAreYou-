import csv
import sys
import re

def ParseCSV(filename):
    mainCharacters = {'Stan', 'Kyle', 'Cartman', 'Kenny', 'Butters', 'Wendy'
    , 'Jimmy','Garrison', 'Mackey', 'Slave', 'Victoria', 'Ned', 'Mayor', 'Satan'}


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
                    if (row[3]) not in wf:
                        wf.write(row[3])
                        wf.close()
                    wfall.write(character + '\t' + row[3])
                    wf.close()
                else:
                    for c in mainCharacters:
                        if c in character:
                            wf = open("char_scripts/" + c +".txt", 'a+')
                            if (row[3]) not in wf:
                                wf.write(row[3])
                            wfall.write(character + '\t' + row[3])
                            wf.close()
                wfall.close()
    finally:
        f.close()

if __name__ == '__main__':
    ParseCSV('SouthParkData-master/All-seasons.csv')
