import resolvedor

alg= resolvedor.SA()

layout = 'Layout.txt'
products = 'Products.txt'
order='Instancias/instances_d5_ord30.txt'


file = open(layout, 'r')
arq2 = file.read().splitlines()
file = open(products, 'r')
arq3 = file.read().splitlines()

file = open(order, 'r')
arq = file.read().splitlines() 
alg.arm.leitura(arq2,arq3,arq)

alg.sa()