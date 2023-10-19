import resolvedor5
alg= resolvedor5.SA()

layout = 'Layout.txt'#'01.txt'
products = 'Products.txt'#'02.txt'
order= 'Instancias/instances_d5_ord5.txt'#'03.txt'


file = open(layout, 'r')
arq2 = file.read().splitlines()
file = open(products, 'r')
arq3 = file.read().splitlines()

file = open(order, 'r')
arq = file.read().splitlines() 
alg.arm.leitura(arq2,arq3,arq)

alg.sa()