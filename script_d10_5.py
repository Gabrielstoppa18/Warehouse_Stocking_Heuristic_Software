import resolvedor4
import numpy as np
import time

alg= resolvedor4.SA()

it=1
tempot = 0
custot = 0
custo = []
custob = 100000
layout = 'Layout.txt'
products = 'Products.txt'

file = open(layout, 'r')
arq2 = file.read().splitlines()
file = open(products, 'r')
arq3 = file.read().splitlines()

arquivo = open('instancias_d10_Resolvedor4_5.txt','w')
arquivo.close()

arquivo = open('instancias_d10_Resolvedor4_5.txt','a')
caminho = 'Instancias'
file = '/instances_d10_ord'
inst = []
for k in range(5,16):
    
    inst.append(caminho+file+str(k)+'.txt')
for i in range(len(inst)):
    tempot = 0
    custot = 0
    custo = []
    custob = 0
    alg.arm.clear()
    alg.clear()
    file = open(inst[i], 'r')
    arq = file.read().splitlines() 
    alg.arm.leitura(arq2,arq3,arq)
    
    for j in range(it):
        timer_inicio = time.perf_counter()
        custo.append(alg.sa())
        timer_fim = time.perf_counter()
        tempoTotal = timer_fim-timer_inicio
        tempot+=tempoTotal        
        print(j)
    custob=min(custo)
    tempom=tempot/it
    custom = np.mean(custo)
    arquivo.write(inst[i]+"&"+str(tempom)+"&"+str(custom)+"&"+str(custob)+"\n")
arquivo.close()
