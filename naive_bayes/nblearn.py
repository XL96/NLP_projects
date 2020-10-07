import sys
import os
import re

train_folder = sys.argv[1]
corpus = {}
negative_truthful = {}
negative_deceptive = {}
positive_truthful = {}
positive_deceptive = {}
NT = 0
ND = 0
PT = 0
PD = 0

for item in os.listdir(train_folder):
    if("negative" in item):
        for sub in os.listdir(train_folder+"/"+item):
            if("truthful" in sub):
                for fold in os.listdir(train_folder+"/"+item +"/"+sub):
                    if("fold" in fold):
                        for file in os.listdir(train_folder+"/"+item +"/"+sub+"/"+fold):
                            data = open (train_folder+"/"+item +"/"+sub+"/"+fold+"/"+file , 'r')
                            for line in data:
                                line = re.sub('[^A-Za-z0-9]+', ' ', line)
                                for word in line.split():
                                    word = word.lower()
                                    NT += 1
                                    if word not in corpus:
                                        corpus[word] = 1
                                    else:
                                        corpus[word] += 1
                                    if word not in negative_truthful:
                                        negative_truthful[word] = 1
                                    else:
                                        negative_truthful[word] += 1
        
            if("deceptive" in sub):
                for fold in os.listdir(train_folder+"/"+item +"/"+sub):
                    if("fold" in fold):
                        for file in os.listdir(train_folder+"/"+item +"/"+sub+"/"+fold):
                            data = open (train_folder+"/"+item +"/"+sub+"/"+fold+"/"+file , 'r')
                            for line in data:       
                                line = re.sub('[^A-Za-z0-9]+', ' ', line)
                                for word in line.split():
                                    word = word.lower()
                                    ND += 1
                                    if word not in corpus:
                                        corpus[word] = 1
                                    else:
                                        corpus[word] += 1
                                    if word not in negative_deceptive:
                                        negative_deceptive[word] = 1
                                    else:
                                        negative_deceptive[word] += 1
                            
    if("positive" in item):
        for sub in os.listdir(train_folder+"/"+item):
            if("truthful" in sub):
                for fold in os.listdir(train_folder+"/"+item +"/"+sub):
                    if("fold" in fold):
                        for file in os.listdir(train_folder+"/"+item +"/"+sub+"/"+fold):
                            data = open (train_folder+"/"+item +"/"+sub+"/"+fold+"/"+file , 'r')
                            for line in data: 
                                line = re.sub('[^A-Za-z0-9]+', ' ', line)
                                for word in line.split():
                                    word = word.lower()
                                    PT += 1
                                    if word not in corpus:
                                        corpus[word] = 1
                                    else:
                                        corpus[word] += 1
                                    if word not in positive_truthful:
                                        positive_truthful[word] = 1
                                    else:
                                        positive_truthful[word] += 1
            if("deceptive" in sub):
                for fold in os.listdir(train_folder+"/"+item +"/"+sub):
                    if("fold" in fold):
                        for file in os.listdir(train_folder+"/"+item +"/"+sub+"/"+fold):
                            data = open (train_folder+"/"+item +"/"+sub+"/"+fold+"/"+file , 'r')
                            for line in data:  
                                line = re.sub('[^A-Za-z0-9]+', ' ', line)
                                for word in line.split():
                                    PD += 1
                                    word = word.lower()
                                    if word not in corpus:
                                        corpus[word] = 1
                                    else:
                                        corpus[word] += 1
                                    if word not in positive_deceptive:
                                        positive_deceptive[word] = 1
                                    else:
                                        positive_deceptive[word] += 1

output = open ('nbmodel.txt' , 'w')      
output.write('token    nt    nd    pt    pd    total\n')

sorted_corpus = sorted(corpus.items(), key=lambda x: x[1], reverse=True)

stopwords = ["the", "and", "to", "a", "i", "was", "in", "of", "for", "at", "we", "is", "that", "were", "with", "as", "so", "are", "an", "it", "you", "they", "he", "she", "them", "him", "her"]

for item in sorted_corpus:
    nt = 1  
    nd = 1
    pt = 1
    pd = 1
    token = item[0]
    if(token in stopwords):
        continue
    if token in negative_truthful:
        nt += negative_truthful[token]
    if token in negative_deceptive:
        nd += negative_deceptive[token]
    if token in positive_truthful:
        pt += positive_truthful[token]
    if token in positive_deceptive:
        pd += positive_deceptive[token]
    output.write(token + '\t' + str((nt + nd)/(ND + NT + len(corpus))) + '\t' + str((pt + pd)/(PT + PD + len(corpus))) + '\t' + str((nt + pt)/(NT + PT + len(corpus))) + '\t' + str((nd + pd)/(ND + PD + len(corpus))) + '\n')
output.close()