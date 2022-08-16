import resolvedor
import time

alg= resolvedor.SA()


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

arquivo = open('instancias_d5.txt','w')
arquivo.close()

arquivo = open('instancias_d5.txt','a')
caminho = 'Instancias'
file = '\instances_d5_ord'
inst = []
for k in range(5,31):
    print(k)
    inst.append(caminho+file+str(k)+'.txt')
for i in range(len(inst)):
    alg.arm.clear()
    file = open(inst[i], 'r')
    arq = file.read().splitlines() 
    alg.arm.leitura(arq2,arq3,arq)
    print(alg.arm.ordens)
    for j in range(1):
        timer_inicio = time.perf_counter()
        custo.append(alg.sa())
        timer_fim = time.perf_counter()
        tempoTotal = timer_fim-timer_inicio
        tempot+=tempoTotal
        custot+=custo[j]
        if custo[j]<custob:
            custob = custo[j]
        print(j)
    tempom=tempot/5
    custom = custot/5
    arquivo.write(inst[i]+"&"+str(tempom)+"&"+str(custom)+"&"+str(custob)+"\n")
arquivo.close()