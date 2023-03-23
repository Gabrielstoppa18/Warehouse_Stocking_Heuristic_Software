import numpy as np
import csv
np.set_printoptions(threshold=np.inf)

qt_prod1=np.zeros(1560)
qt_prod2=np.zeros(1560)
qt_prod3=np.zeros(1560)
id_prod=np.arange(1,1561)

for i in range(1,27):
    a=str(i)
    filepath3 = "data/1"+"/"+a+".txt"
    file3 = open(filepath3, 'r')
    arq = file3.read().splitlines()
    qt_ord=int(arq[0])
    
    for j in range(2,qt_ord+2):
        inf=arq[j].split()
        totprod = int(inf[0])
        for j in range(0,totprod*2,2):
            ids=int(inf[1+j])
            qt=int(inf[2+j])
            qt_prod1[ids-1]+=qt

for i in range(1,27):
    a=str(i)
    filepath3 = "data/2"+"/"+a+".txt"
    file3 = open(filepath3, 'r')
    arq = file3.read().splitlines()
    qt_ord=int(arq[0])
    
    for j in range(2,qt_ord+2):
        inf=arq[j].split()
        totprod = int(inf[0])
        for j in range(0,totprod*2,2):
            ids=int(inf[1+j])
            qt=int(inf[2+j])
            qt_prod2[ids-1]+=qt

for i in range(1,27):
    a=str(i)
    filepath3 = "data/3"+"/"+a+".txt"
    file3 = open(filepath3, 'r')
    arq = file3.read().splitlines()
    qt_ord=int(arq[0])
    
    for j in range(2,qt_ord+2):
        inf=arq[j].split()
        totprod = int(inf[0])
        for j in range(0,totprod*2,2):
            ids=int(inf[1+j])
            qt=int(inf[2+j])
            qt_prod3[ids-1]+=qt

with open('dados.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Produtos', '1', '2', '3'])
    for i in range(len(id_prod)):
        writer.writerow([id_prod[i], qt_prod1[i], qt_prod2[i], qt_prod3[i]])