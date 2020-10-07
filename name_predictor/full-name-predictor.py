import sys
import numpy as np

male = np.genfromtxt('dist.male.first.txt', dtype = str)
female = np.genfromtxt('dist.female.first.txt', dtype = str)
male_name = []
female_name = []
    
for x in male:
    male_name.append(x[0])
    
for x in female:
    female_name.append(x[0])

if __name__ == "__main__":
    data = np.genfromtxt(sys.argv[1], delimiter=',', dtype = str)

    f = open("full-name-output.csv", "a")
    for record in data:
        names = record.split(" AND ")
        p1 = names[0].split()
        p2 = names[1].split()
        name = ""
        if("PROFESSOR" in p1 or "PROFESSOR" in p2):
            name = names[0]
        elif("DOCTOR" in p1 or "DOCTOR" in p2):
            name = names[0]
        elif(p1[-1] not in male_name and p1[-1] not in female_name):
            name = names[0]
        elif(len(p1) >= 3):
            name = names[0]
        elif(len(p1) == 1):
            if(p2[len(p2)-2] not in male_name and p2[len(p2)-2] not in female_name):     
                name = names[0] + ' ' + p2[len(p2)-2] + ' ' + p2[-1]  
            else:
                name = names[0] + ' ' + p2[-1] 
        elif(len(p1) < len(p2)):
            if(p2[len(p2)-2] not in male_name and p2[len(p2)-2] not in female_name):
                name = names[0] + ' ' + p2[len(p2)-2] + ' ' + p2[-1]  
            else:
                name = names[0] + ' ' + p2[-1] 
        else:
            name = names[0] + ' ' + p2[-1] 
        
        f.writelines(record + ',' + name + '\n')
            

        
    
    f.close()