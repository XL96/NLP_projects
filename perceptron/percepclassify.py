import sys
import os
import re
import math

test_folder = sys.argv[2]
modelfile = open(sys.argv[1], 'r')

TD_vector = {}
NP_vector = {}


firstline = modelfile.readline().strip().split('\t')
b1 = firstline[1]
b2 = firstline[3]


output = open ('percepoutput.txt' , 'w')

for line in modelfile:
    if re.search ('\t' , line):
        weights = line.strip().split('\t')
        TD_vector[weights[0]] = weights[1]
        NP_vector[weights[0]] = weights[2]
 



for subfolder in os.listdir(test_folder):
    if(os.path.isdir(test_folder + '/' + subfolder)):
        for items in os.listdir(test_folder + '/' + subfolder):
            for fold in os.listdir(test_folder + '/' + subfolder + '/' + items):
                for file in os.listdir(test_folder + '/' + subfolder + '/' + items + '/' + fold):

                    td = float(b1)
                    np = float(b2)

                    data = open(test_folder + '/' + subfolder + '/' + items + '/' + fold + '/' + file , 'r')
                    words = {}
                    for line in data:
                        line = re.sub('[^A-Za-z0-9]+', ' ', line)
                        for word in line.split():
                            word = word.lower()
                            if word in words:
                                words[word] += 1
                            else:
                                words[word] = 1
                    for i in words:
                        if i in TD_vector:
                            td += float(TD_vector[i]) * words[i]
                        if i in NP_vector: 
                            np += float(NP_vector[i]) * words[i]
                                
                    labela = 'truthful'
                    labelb = 'positive'
                    
                    if(td < 0):
                        labela = "deceptive"
                    if(np < 0):
                        labelb = "negative"
                    
                    output.write(labela + " " + labelb + " " + test_folder + '/' + subfolder + '/' + items + '/' + fold + '/' + file + '\n')
                
                        
output.close()