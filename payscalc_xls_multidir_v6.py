# Dolgopolov A

# Month calculation script

# Calculate pays reestr files in set of directories from diferent pays agents
# at start you need to enter month number in two digits format, like "02"
# Script looks through all elements of current folder (where it was executed)
# and if finds folder with name like *.[0-9][0-9].* it begins to read files in it
# and process them.

from pathlib import Path
from decimal import *
import os
import csv
import re

print('\n* * * Вычисление суммы за указанный месяц * * *')
print('\nВсе папки с файлами для расчета должны находится в папке где находится данный скрипт')
print ('\nВведите номер месяца в формате двух цифр \nНапример(01):')
xMonth = input()


paydir = Path.cwd()

totalfies = 0
totalHSum = 0 # total from all header summs of all files
totalLSum = 0 # total calculated from all lines in all files
agent_collector = []

for directory in os.listdir(paydir):
    print(directory)
    if os.path.isdir(directory):
        print('dir')
        if re.match('.*\.[01][1-9]\..*',directory) and directory.split('.')[1] == xMonth:
            print('- > > calculating:')
            for filename in os.listdir(paydir / directory):
                
                #loop files
                csvreader = None
                print(filename)
                agent_collector += [[filename]]
                mfile = open(paydir /directory/ filename)

                #agent
                #print(filename[0:1])
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
                #DEBUG
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

                
        else:
            print('- - skip by filename pattern')
    else:
        print('\ not dir --skip')

        print('Almost done...')
        
        
    print('total dir sum: ' + str(totalLSum))  
    print('total dir files:' + str(totalfies) + '\n')
print(' - - - End dir processing loop - - -')
#print(agent_collector) # enable to DEBUG
print('\nTOTAL SUM: ' + str(totalLSum))
print('TOTAL FILES:' + str(totalfies) + '\n')

#write CSV file result
outputDir = Path.cwd()
#os.mkdir(outputDir)
outputFile = open(str(outputDir) + '/месяц_' + xMonth + '_total.csv','w',newline='')
outputWriter = csv.writer(outputFile, delimiter = ';')
outputWriter.writerows(agent_collector)
outputFile.close()

print('Работа завершена!')

    
