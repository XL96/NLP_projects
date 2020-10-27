import sys

train_data = open(sys.argv[1], 'r')
emission = {}
transition = {}
transition['start'] = {}
transition['start']['total'] = 0
tags = {}

for lines in train_data:
    words = lines.split()
    for i in range(len(words)):
        token = words[i].split('/')
        if len(token) > 2:
            for j in range(1,len(token) - 1):
                token[0] += ('/' + token[j])
            token[1] = token[-1]
        token[0] = token[0].lower()
        
        #update emmision model
        if token[1] not in emission:
            emission[token[1]] = {}
            emission[token[1]][token[0]] = 1
            emission[token[1]]['total'] = 0
        elif token[0] not in emission[token[1]]:
            emission[token[1]][token[0]] = 1
        else:
            emission[token[1]][token[0]] += 1
        emission[token[1]]['total'] += 1
        
        #update transition model
        if token[1] not in tags:
            tags[token[1]] = 1
        else:
            tags[token[1]] += 1
        if token[1] not in transition:
            transition[token[1]] = {}
            transition[token[1]]['total'] = 1
        else:
            transition[token[1]]['total'] += 1
        if i == 0:
            if token[1] not in transition['start']:
                transition['start'][token[1]] = 1
            else:
                transition['start'][token[1]] += 1
            transition['start']['total'] += 1
        else:
            lastToken = words[i - 1].split('/')
            if len(lastToken) > 2:
                for j in range(1,len(lastToken) - 1):
                    lastToken[0] += ('/' + lastToken[j])
                lastToken[1] = lastToken[-1] 
            if token[1] not in transition[lastToken[1]]:
                transition[lastToken[1]][token[1]] = 1
            else:
                transition[lastToken[1]][token[1]] += 1

#Add one smoothing transitions:
for tag in tags:
    if tag not in transition:
        transition[tag] = {}
        transition['total'] = 1

for prev in transition:
    for tag in tags:
        if tag not in transition[prev]:
            transition[prev][tag] = 1
            transition[tag]['total'] += 1
            
        

output = open('hmmmodel.txt', 'w')


output.write('Transition Model: \n')
for tag in transition:
    output.write(tag + ' ')
    for item in transition[tag]:
        if(item != 'total'):
            output.write(item + ':' + str(transition[tag][item]/transition[tag]['total']) + ' ')
    output.write('\n')
    
output.write('Emission Model: \n')
for word in emission:
    output.write(word + ' ')
    for tag in emission[word]:
        if(tag != 'total'):
            output.write(tag + ':' + str(emission[word][tag]/emission[word]['total']) + ' ')
    output.write('\n')

output.write('Tags: \n')
for tag in tags:
    output.write(tag + ':' + str(tags[tag]) + '\n')

output.close()
    
    