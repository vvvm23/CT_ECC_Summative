# 
# Script to test the formatting of your input/output
#
# Instructions:
# 1. Copy this file into the same folder as your main .py file
# 2. In the following line, change "practical" to your file main .py file name

from vvvm23 import *

# 3. Run this file (you can simply double-cick on it in the file explorer)
# It should produce a text file called test.txt
#
# Advice:
# The script will automatically stop if it cannot find the function it is trying to test,
# so just include dummy functions for all the seven functions,
# and make sure all such dummy functions return something ( an empty list [] for instance).
# That way, you will always get the right total marks at the end.
#
# Note that I will use more input/solution pairs when I mark your code.




inputs      = [ [ [1],              [0,0,1] ],          #a
                [ [0],              [0,0,0] ],          #m
                [ [1,1,0],          [1,0,0,0,0,0,0] ],  #v
                [ [1,1,1,1,1,1,1],  [0,0,0,0] ],        #c
                [ [0,0,1,1],        [1,1,1,1] ],        #m
                [ [ [0], 2 ],       [ [1], 4 ]  ],      #m,n
                [ [0,0,1],          [1,1,1,1] ] ]       #v


solutions   = [ [ [0,0,1,1],    [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0] ],    #m
              [ [0,0,0],        [] ],                                   #c
              [ [1,1,1],        [0,0,0,0,0,0,0] ],                      #c
              [ [1,1,1,1],      [] ],                                   #m
              [ [1],            [] ],                                   #a
              [ [0,0],          [1,1,1,1] ],                            #c
              [ [0],            [1] ] ]                                 #m

marks       = [10, 10, 30, 10, 20, 10, 10]

myMarks     = marks

outfile     = open('test.txt', 'w')

title       = 'Error-Correcting codes 2018-19\n\nTest Results\n\n'
outfile.write(title)


for i in range(7):

    title = ['\n \nPart 0. message(a)\n\n',
             '\n \nPart 1. hammingEncoder(m)\n\n',
             '\n \nPart 2. hammingDecoder(v)\n\n',
             '\n \nPart 3. messageFromCodeword(c)\n\n',
             '\n \nPart 4. dataFromMessage(m)\n\n',
             '\n \nPart 5. repetitionEncoder(m,n)\n\n',
             '\n \nPart 6. repetitionDecoder(v)\n\n' ]

    outfile.write(title[i])

    
    for j in range(2):

        outcome     = ''
        testOutcome = ''

        if i == 0:
            testOutput = message(inputs[i][j])
        if i == 1:
            testOutput = hammingEncoder(inputs[i][j])
        if i == 2:
            testOutput = hammingDecoder(inputs[i][j])
        if i == 3:
            testOutput = messageFromCodeword(inputs[i][j])
        if i == 4:
            testOutput = dataFromMessage(inputs[i][j])
        if i == 5:
            testOutput = repetitionEncoder(inputs[i][j][0], inputs[i][j][1])
        if i == 6:
            testOutput = repetitionDecoder(inputs[i][j])

     
        if testOutput == solutions[i][j]:
            testOutcome = 'ok\n\n'
        else:
            myMarks[i] = 0
            testOutcome = 'NO\n\n'
     

        inputsString    = str(i) + '.' + str(j) +'.\nInput:\t\t' + str(inputs[i][j]) + '\n'
        outputsString   = 'Output:\t\t' + str(testOutput) + ' \n'
        solutionsString = 'Solution:\t' + str(solutions[i][j]) + ' \n'
        outcomeString   = 'Outcome:\t' + testOutcome

        outcome         = inputsString + outputsString + solutionsString + outcomeString


        outfile.write(outcome)

    marksString = 'Part ' + str(i) + ': ' + str(myMarks[i]) + ' marks\n\n'
    outfile.write(marksString)

myTotalMarks        = sum(myMarks)
totalMarksString    = '\nTOTAL = ' + str(myTotalMarks) + ' MARKS'
outfile.write(totalMarksString)
