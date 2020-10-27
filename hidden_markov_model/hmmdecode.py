import sys
import re
import math

transition = {}
emission = {}
test_data = open(sys.argv[1], 'r')
model = open('hmmmodel.txt').read().splitlines()
tags = {}

i = 1
for line in model[1:]:
    if not re.search('Emission Model', line):
        i += 1
    else:
        break
    tran = line.split()
    transition[tran[0]] = {}
    for tag in tran[1:]:
        prob = tag.split(':')
        transition[tran[0]][prob[0]] = float(prob[1])

i += 1
for line in model[i:]:
    em = line.split()
    if not re.search('Tags', line):
        i += 1
    else:
        break
    for tag in em[1:]:
        prob = tag.split(':')
        if len(prob) > 2:
            for l in range(1, len(prob) - 1):
                prob[0] += prob[l]
            prob[1] = prob[-1]
        if prob[0] not in emission:
            emission[prob[0]] = {}
        emission[prob[0]][em[0]] = float(prob[1])


for line in model[i + 1:]:
    text = line.split(':')
    tags[text[0]] = int(text[1])

totalTags = 0
for tag in tags:
    totalTags += tags[tag]
    
output = open ('hmmoutput.txt' , 'w')
for line in test_data:
    words = line.split()
    last_state = 'start'
    for i in range(len(words)):
        maxProb = 0
        state = ''
        word = words[i].lower()
        if word in emission:
            for tag in emission[word]:
                prob = emission[word][tag] * transition[last_state][tag]
                if prob >= maxProb:
                    maxProb = prob
                    state = tag
                
        else:
            for tag in transition[last_state]:
                #if tag in frequentTag[:8]:
                prob = transition[last_state][tag] * tags[tag] / totalTags
                if prob > maxProb:
                    maxProb = prob
                    state = tag
        output.write(words[i] + '/' + state + ' ')
        last_state = state
    output.write('\n')
output.close()  
