#where to save all files
#work_dir = "C:\\Python\\Python310\\Scripts\\ecopays\\13tail"

from pathlib import Path
from decimal import *
#Path('spam') / 'bacon' / 'eggs'
#Path('spam') / Path('bacon/eggs')
import os
import csv
import re
print (Path.cwd() / '13tail')

f = Path.cwd() / '13tail' / 'E165616_224316665_141972_92.txt'
paydir = Path.cwd() / '13tail'
print (f.stem)
print(f.suffix)
print(f.parents[1])
#print('get size of file: ' + str(os.path.getsize(f)))
print(os.listdir(f / '..'))
totalfies = 0
totalHSum = 0 # total from all header summs of all files
totalLSum = 0 # total calculated from all lines in all files
agent_collector = []
#loop files
print('*\nprocess files')
for filename in os.listdir(f / '..'):
    print(filename)
    agent_collector += [[filename]]
    mfile = open(paydir / filename)
    csvreader = csv.reader(mfile, delimiter = ';')
    xData = list(csvreader)
    rSum = xData[1][0] #sum from file header
    rSumDec = Decimal(rSum[1:]) #cut '#' symbol
    print(rSumDec)
    
    #agent
    
    if re.match('^[a-z]{3}',filename[0:3]):#filename[0:3] == 'tko':
        agent_name = xData[7][0]
        if len(agent_name) < 3:
            agent_name = 'Болотное'
    elif filename[0:1] == 'P':
        agent_name = 'НЭС'
    elif filename[0:1] == '4':
        agent_name = 'Сбербанк'
    else:
        agent_name = xData[6][1]
        #get rid of any shit except Agent name
        agent_name = agent_name[agent_name.find("<")+1:agent_name.find(">")]
    print(agent_name)
    agent_collector[totalfies] += [agent_name]
    
    #sum all lines in current file
    
    ttl = 0
    if filename[0:3] == 'tko' or filename[0:3] == 'tog':
        for xline in xData[8:]: # bolotnoye header ends at 8 line
            ttl = ttl+Decimal(xline[4])
        print('total ' + str(ttl))
        agent_collector[totalfies] += [ttl]
        totalLSum += ttl
    elif agent_name == 'НЭС':
        for xline in xData[:len(xData)-1]:
            ttl = ttl+Decimal(xline[3])
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
    print('total sum: ' + str(totalLSum))    
    totalfies = totalfies + 1
print('\ntotal files:' + str(totalfies))
print(agent_collector)
#efile = open(f)
#eContent = efile.read()
#print('printing:')
#print(eContent)
#result = open('result2.txt', 'w')
#result.write('lemon');
#result.close()



#csv practice
agent_collectorx = []
print()
egorod = open(f)
ttl = 0;
exampleReader = csv.reader(egorod, delimiter = ';')
eData = list(exampleReader)
rSum = eData[1][0] #sum from file header
rSumDec = Decimal(rSum[1:]) #cut '#' symbol
agent_collector = agent_collectorx + [rSumDec]
print (rSumDec)
agent_name = eData[6][1]
#get rid of any shit except Agent name

agent_name = agent_name[agent_name.find("<")+1:agent_name.find(">")]
agent_collectorx = agent_collectorx + [agent_name]
for xline in eData[12:]:
    ttl = ttl+Decimal(xline[3])
print('total ' + str(ttl))
agent_collectorx = agent_collectorx + [ttl]
print(agent_collectorx)
if rSumDec == ttl:
    print('equal')
else:
    print('NOT equal')
    
