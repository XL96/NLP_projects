import sys
import os
import re
import random

train_folder = sys.argv[1]
corpus = set()
TD_vector = {}
NP_vector = {}
TD_vector_average = {}
NP_vector_average = {}
trainning_data = []
stopwords = ["the", "and", "to", "a", "i", "was", "in", "of", "for", "at", "we", "is", "that", "were", "with", "as", "so", "are", "an", "it", "you", "they", "he", "she", "them", "him", "her"]

for item in os.listdir(train_folder):
    if("negative" in item):
        for sub in os.listdir(train_folder+"/"+item):
            if("truthful" in sub):
                for fold in os.listdir(train_folder+"/"+item +"/"+sub):
                    if("fold" in fold):
                        for file in os.listdir(train_folder+"/"+item +"/"+sub+"/"+fold):
                            data = open (train_folder+"/"+item +"/"+sub+"/"+fold+"/"+file , 'r')
                            record = {}
                            for line in data:
                                line = re.sub('[^A-Za-z0-9]+', ' ', line)
                                for word in line.split():
                                    word = word.lower()
                                    #if(word not in stopwords):
                                    if(word not in corpus):
                                        corpus.add(word)
                                    if(word in record):
                                        record[word] += 1
                                    else:
                                        record[word] = 1
                            trainning_data.append([1, record])
        
            if("deceptive" in sub):
                for fold in os.listdir(train_folder+"/"+item +"/"+sub):
                    if("fold" in fold):
                        for file in os.listdir(train_folder+"/"+item +"/"+sub+"/"+fold):
                            data = open (train_folder+"/"+item +"/"+sub+"/"+fold+"/"+file , 'r')
                            record = {}
                            for line in data:
                                line = re.sub('[^A-Za-z0-9]+', ' ', line)
                                for word in line.split():
                                    word = word.lower()
                                    #if(word not in stopwords):
                                    if(word not in corpus):
                                        corpus.add(word)
                                    if(word in record):
                                        record[word] += 1
                                    else:
                                        record[word] = 1
                            trainning_data.append([2, record])
                            
    if("positive" in item):
        for sub in os.listdir(train_folder+"/"+item):
            if("truthful" in sub):
                for fold in os.listdir(train_folder+"/"+item +"/"+sub):
                    if("fold" in fold):
                        for file in os.listdir(train_folder+"/"+item +"/"+sub+"/"+fold):
                            data = open (train_folder+"/"+item +"/"+sub+"/"+fold+"/"+file , 'r')
                            record = {}
                            for line in data:
                                line = re.sub('[^A-Za-z0-9]+', ' ', line)
                                for word in line.split():
                                    word = word.lower()
                                    #if(word not in stopwords):
                                    if(word not in corpus):
                                        corpus.add(word)
                                    if(word in record):
                                        record[word] += 1
                                    else:
                                        record[word] = 1
                            trainning_data.append([3, record])
            if("deceptive" in sub):
                for fold in os.listdir(train_folder+"/"+item +"/"+sub):
                    if("fold" in fold):
                        for file in os.listdir(train_folder+"/"+item +"/"+sub+"/"+fold):
                            data = open (train_folder+"/"+item +"/"+sub+"/"+fold+"/"+file , 'r')
                            record = {}
                            for line in data:
                                line = re.sub('[^A-Za-z0-9]+', ' ', line)
                                for word in line.split():
                                    word = word.lower()
                                    #if(word not in stopwords):
                                    if(word not in corpus):
                                        corpus.add(word)
                                    if(word in record):
                                        record[word] += 1
                                    else:
                                        record[word] = 1
                            trainning_data.append([4, record])

random.shuffle(trainning_data)    

def train_vanilla(vector, b, data, model, itr):
    for itr in range(itr):
        random.shuffle(trainning_data)  
        for item in data:
            a = b
            y = 0
            if(model == "NP"):
                if(item[0] == 3 or item[0] == 4):
                    y = 1
                else:
                    y = -1
            else:
                if(item[0] == 1 or item[0] == 3):
                    y = 1
                else:
                    y = -1
                    
            
            for word in item[1]:
                if word in vector and word not in stopwords:
                    a += item[1][word] * vector[word]
                else:
                    vector[word] = 0
            if(a * y <= 0):

                b = b + y
                for word in item[1]:
                    vector[word] += item[1][word] * y
    return vector, b


def train_average(vector, b, data, model, itr):
    Cached_vector = {}
    Cached_b = 0
    c = 1
    #vanilla_vector = {}
    #vanilla_b = b
    for itr in range(itr):
        random.shuffle(trainning_data)  
        for item in data:
            a = b
            y = 0
            if(model == "NP"):
                if(item[0] == 3 or item[0] == 4):
                    y = 1
                else:
                    y = -1
            else:
                if(item[0] == 1 or item[0] == 3):
                    y = 1
                else:
                    y = -1 
            for word in item[1]:
                if word in vector and word not in stopwords:
                    a += item[1][word] * vector[word]
                else:
                    Cached_vector[word] = 0
                    vector[word] = 0
            if(a * y <= 0):
                b = b + y
                Cached_b += y * c
                for word in item[1]:
                    vector[word] += item[1][word] * y
                    Cached_vector[word] += item[1][word] * y * c
            c += 1
    #vanilla_b = b
    b -= float(Cached_b / c)
    for i in vector:
        #vanilla_vector[i] = vector[i]
        vector[i] -= float(Cached_vector[word]/c)
    return vector, b

TD_vector, b1 = train_vanilla(TD_vector, 0, trainning_data, "TD", 30)
NP_vector, b2 = train_vanilla(NP_vector, 0, trainning_data, "NP", 30)
TD_vector_average, b1_average = train_average(TD_vector_average, 0, trainning_data, "TD", 90)
NP_vector_average, b2_average = train_average(NP_vector_average, 0, trainning_data, "NP", 90)




def write_model(file_name, vector1, vector2, corpus):
    output = open(file_name, 'w')
    output.write('TD_b\t' + str(b1) + '\tNP\t' + str(b2) +'\n')
    output.write('word    TD_weights    NP_weights')
    for word in corpus:
        w1 = vector1[word]
        w2 = vector2[word]
        output.write(word + '\t' + str(w1) + '\t' + str(w2) + '\n')

write_model('vanillamodel.txt', TD_vector, NP_vector, corpus)
write_model('averagedmodel.txt', TD_vector_average, NP_vector_average, corpus)
