#where to save all files
#work_dir = "C:\\Python\\Python310\\Scripts\\ecopays\\13tail"

from pathlib import Path
from decimal import *
import os
import csv
import re

print ('Input directory name:')
xDir = input()

paydir = Path.cwd() / xDir
#print (f.stem)
#print(f.suffix)
#print(f.parents[1])
#print('get size of file: ' + str(os.path.getsize(f)))
#print(os.listdir(f / '..'))
totalfies = 0
totalHSum = 0 # total from all header summs of all files
totalLSum = 0 # total calculated from all lines in all files
agent_collector = []
#loop files
print('* * * \nprocess files:\n')
for filename in os.listdir(paydir):
    csvreader = None
    print(filename)
    agent_collector += [[filename]]
    mfile = open(paydir / filename) 
    
    #agent
    print(filename[0:1])
    
    if re.match('^[a-z]{3}',filename[0:3]): # bolotnoye and toguchin
        paysystem = 'Болотное_Тогучин'
        csvreader = csv.reader(mfile, delimiter = ';')
        xData = list(csvreader)
        agent_name = xData[7][0]
        if len(agent_name) < 3:
            agent_name = 'Болотное'
        #summa header from file
        rSum = xData[1][0] #sum from file header
        rSumDec = Decimal(rSum[1:]) #cut '#' symbol
        print(rSumDec)
        agent_collector[totalfies] += [paysystem]
    elif filename[0:1] == 'P':
        paysystem = 'НЭС'
        csvreader = csv.reader(mfile, delimiter = '|')
        xData = list(csvreader)
        #agent_name = 'НЭС'
        agent_name = xData[len(xData)-1][5]
        rSum = xData[len(xData)-1][2] #sum from file header
        rSumDec = Decimal(rSum)
        print('hSum:' + str(rSumDec))
        agent_collector[totalfies] += [paysystem]
    elif filename[0:1] == '4':
        paysystem = 'Сбербанк'
        csvreader = csv.reader(mfile, delimiter = ';')
        xData = list(csvreader)
        agent_name = 'Сбербанк'
        agent_collector[totalfies] += [paysystem]
    else:
        paysystem = 'Город'
        csvreader = csv.reader(mfile, delimiter = ';')
        xData = list(csvreader)
        agent_name = xData[6][1]
        #get rid of any shit except Agent name
        agent_name = agent_name[agent_name.find("<")+1:agent_name.find(">")]
        agent_collector[totalfies] += [paysystem]
    print(agent_name)
    agent_collector[totalfies] += [agent_name]
    
    #sum all lines in current file
    #DEBUH
    ttl = 0
    if filename[0:3] == 'tko' or filename[0:3] == 'tog':
        for xline in xData[8:]: # bolotnoye header ends at 8 line
            ttl = ttl+Decimal(xline[4])
        print('total ' + str(ttl))
        agent_collector[totalfies] += [ttl]
        totalLSum += ttl
    elif paysystem == 'НЭС':
        for xline in xData[:len(xData)-1]:
            ttl = ttl + Decimal(xline[3])
        print('total ' + str(ttl))
        agent_collector[totalfies] += [ttl]
        totalLSum += ttl
    elif paysystem == 'Сбербанк':
        for xline in xData[:len(xData)-2]:
            ttl = ttl + Decimal(xline[9])
        print('total ' + str(ttl))
        agent_collector[totalfies] += [ttl]
        totalLSum += ttl
    else:
        for xline in xData[12:]: # Gorod System header ends at 12 line number
            ttl = ttl+Decimal(xline[3])
        print('total ' + str(ttl))
        agent_collector[totalfies] += [ttl]
        totalLSum += ttl
    print()  
    totalfies = totalfies + 1
    
print('total sum: ' + str(totalLSum))  
print('\ntotal files:' + str(totalfies))
print(agent_collector)

#write CSV file result
outputFile = open(str(paydir) + '\\' + xDir + '_result.csv','w',newline='')
outputWriter = csv.writer(outputFile, delimiter = ';')
outputWriter.writerows(agent_collector)
outputFile.close()

#efile = open(f)
#eContent = efile.read()
#print('printing:')
#print(eContent)
#result = open('result2.txt', 'w')
#result.write('lemon');
#result.close()

    
