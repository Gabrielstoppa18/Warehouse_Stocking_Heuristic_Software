import resolvedor5
alg= resolvedor5.SA()

layout = '01.txt'#'Layout.txt'
products = '02.txt'#'Products.txt'
order= '03.txt'#'Instancias/instances_d5_ord5.txt'


file = open(layout, 'r')
arq2 = file.read().splitlines()
file = open(products, 'r')
arq3 = file.read().splitlines()

file = open(order, 'r')
arq = file.read().splitlines() 
alg.arm.leitura(arq2,arq3,arq)

alg.sa()