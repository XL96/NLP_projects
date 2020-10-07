import sys
import os
import re
import math

test_folder = sys.argv[1]

modelfile = open('nbmodel.txt' , 'r')

model = {}


for line in modelfile:
    if re.search ('\t' , line):
        features = line.strip().split('\t')
        model[features[0]] = [float(features[1]), float(features[2]), float(features[3]), float(features[4])]

 

output = open ('nboutput.txt' , 'w')

for subfolder in os.listdir(test_folder):
    if(os.path.isdir(test_folder + '/' + subfolder)):
        for items in os.listdir(test_folder + '/' + subfolder):
            for fold in os.listdir(test_folder + '/' + subfolder + '/' + items):
                for file in os.listdir(test_folder + '/' + subfolder + '/' + items + '/' + fold):
                    
                    negative = math.log(0.5)
                    positive = math.log(0.5)
                    truthful = math.log(0.5)
                    deceptive = math.log(0.5)
                    """
                    nt = math.log(0.25)
                    pt = math.log(0.25)
                    nd = math.log(0.25)
                    pd = math.log(0.25)
                    """
                    data = open(test_folder + '/' + subfolder + '/' + items + '/' + fold + '/' + file , 'r')
                    for line in data:
                        line = re.sub('[^A-Za-z0-9]+', ' ', line)
                        for word in line.split():
                            word = word.lower()
                            if word in model:
                                
                                negative += math.log(model[word][0])
                                positive += math.log(model[word][1])
                                truthful += math.log(model[word][2])
                                deceptive += math.log(model[word][3])
                                
                    labela = 'truthful'
                    labelb = 'positive'
                    if(negative > positive):
                        labelb = "negative"
                    if(deceptive > truthful):
                        labela = "deceptive"
                    
                    output.write(labela + " " + labelb + " " + test_folder + '/' + subfolder + '/' + items + '/' + fold + '/' + file + '\n')
                
                        
output.close()