### WARNING! CONTAINS OBSCENE AMOUNTS PROFANITIES. NOT SAFE FOR KIDS! ###

How to run the Classifier program:
  Step 1.) Go to the directory the final Project folder is saved in.
  Step 2.) Run runthisscript.txt by typing in the following
          ie.   python3 runthisscript.txt

           This file will run the commands to parse the raw files as well as the csv files
           in order to generate the files needed for the program to run.

  Step 3.) run characters.py on a given president. This will tell you the numerical value of the
           president's given attributes.

           ie.  python3 characters.py DonaldTrump
                python3 characters.py BarackObama
                python3 characters.py GeorgeBush

           The program will then compare the output numerical values with the values
           of each south park characters and will give you the result of the closest match.


How to run the Sentence Generator:
  Step 1.) In the directory where the Project is saved, type in the following commands:
          ie.  python3 sentenceGenerator.py

          This would generate a group of files in the generate scripts directory and these files would contain
          the randomly generated sentences for each character. This command is only use to generate the files that
          are then used in the classifier
  Step 2.) If you simply want to play around with the sentence generator, simply use the following command
          ie. python3 sentenceGenerator.py Kyle 3

          where Kyle is the SouthPark character's name and 3 is the length of the chain.
          These 2 inputs, are completely option although the character name has to be given in order to generate on one sentence
          just to play around with the program.
