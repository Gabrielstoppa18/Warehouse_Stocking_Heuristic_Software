from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt

#import matplotlib.pyplot as plt
#import sympy as sp
import numpy as np
from tkinter import filedialog



class Armazem:
    def __init__(self):
        self.A = nx.Graph()
        self.numAisles = 0
        self.numShelves = 0
        self.numLocPerAisleSide = 0
        self.totalLocations = 0
        self.totalvertices = 0
        self.numProdVertices = 0
        self.totalpro=0
        self.totalord=0
        self.ordens=[]
        self.qtprod=[]
        self.vertPos= [(0,0)]
        self.po=[Produto()]
        self.ord=[Ordem()]
        self.nome = ""
        self.loc=[]
        self.dist=[]
    def clear(self):
        self.A = nx.Graph()
        self.numAisles = 0
        self.numShelves = 0
        self.numLocPerAisleSide = 0
        self.totalLocations = 0
        self.totalvertices = 0
        self.numProdVertices = 0
        self.totalpro=0
        self.totalord=0
        self.ordens=[]
        self.qtprod=[]
        self.vertPos= [(0,0)]
        self.po=[Produto()]
        self.ord=[Ordem()]
        self.nome = ""
        self.loc=[]
        self.dist=[]
    def leitura(self,arq1,arq2,arq3):

        self.clear()
        a= arq1[1].split()
        b= arq1[3].split()
        c=arq1[12].split()
        d=arq1[13].split()
        e=arq1[14].split()
        f=arq1[15].split()

        self.numAisles = int(a[1])
        self.numShelves = int(b[1])
        self.numLocPerAisleSide = int(c[1])
        self.totalLocations = int(d[1])
        self.totalvertices = int(e[1])
        self.numProdVertices =int(f[1])

        for x in range(1608,1608+self.numProdVertices):
            a = arq1[x].split()
            posx = int(a[1])
            posy = int(a[2])
            tupla=[posx,posy]
            self.vertPos.append(tupla)
        for x in range(1875,1875+24):
            #1875,1875+24
            a = arq1[x].split()
            posx = int(a[1])
            posy = int(a[2])
            tupla=[posx,posy]
            self.vertPos.append(tupla)
        
        a= 1903
        #a= 1623
        for i in range(a,a+self.numProdVertices):
            loc0=[]
            k = arq1[i].split()
            for j in range(2,8):
                #2,8
                loc0.append(int(k[j]))
            self.loc.append(loc0)
        

        for i in range(self.totalvertices):
            self.A.add_node(i,pos=(self.vertPos[i][0],self.vertPos[i][1]))
        
        a=2194
        #a=1632
        for i in range(a,a+self.totalvertices):
            k = arq1[i].split()
            for j in range(0,int(k[1])+1,2):
                self.A.add_edge(int(k[0]),int(k[j+2]),weight=float(k[j+3]))


        self.dist=dict(nx.all_pairs_dijkstra_path_length(self.A))     

        self.totalpro= int(arq2[0])
        for i in range(self.totalpro):
            self.po.append(Produto())

        d=2
        for i in range(self.totalpro):
            inf = arq2[d].split()
            inf2=inf[0].split(',')
            self.po[i].idprod = int(inf2[0])

            d+=1
        
        self.totalord= int(arq3[0])
        for i in range(self.totalord):
            self.ord.append(Ordem())
        b=2
        for i in range(self.totalord):
            inf = arq3[b].split()
            self.ord[i].totprod = int(inf[0])
            for j in range(0,self.ord[i].totprod*2,2):
                tupla=(int(inf[1+j]),i,0)
                self.ordens.append(tupla)
                self.ord[i].lprod.append(int(inf[1+j]))
            for j in range(1,self.ord[i].totprod*2+1,2):
                tupla=(int(inf[1+j]),i,0)
                self.qtprod.append(tupla)
                self.ord[i].qtprod.append(int(inf[1+j]))
            
            b+=1
        #print(self.qtprod, self.ordens)    
    def imprimir(self):
        with open('entrada.txt','w')as entrada:
            entrada.write("Entrada: "+str(self.nex)+" "+ str(self.ney)+" "+ str(self.nez)+"\n")
            entrada.write("Saida: "+str(self.nsx)+" "+ str(self.nsy)+" "+ str(self.nsz)+"\n")
            entrada.write("Espacos de alocacao: "+str(self.prt*self.cel)+"\n")
            entrada.write("Prat: "+str(self.prt)+"\n")
            entrada.write("Cel: "+str(self.cel)+"\n")
            for i in range(self.prt):
                for j in range(self.cel):
                    entrada.write("ID da celula:"+str(self.pa[i].pra[j].idcel)+ " "+ "X/Y/Z: "+str(self.pa[i].pra[j].xcel)+" "+str(self.pa[i].pra[j].ycel)+" "+str(self.pa[i].pra[j].zcel)+"\n")
            entrada.write("Total de produtos:"+str(self.totalpro)+"\n")
            entrada.write("Produtos: \n")
            for i in range(self.totalpro):
                entrada.write(str(self.po[i].idprod)+"\n")
            entrada.write("Total de ordens:"+str(self.totalord)+"\n")
            for i in range(self.totalord):
                entrada.write(str(self.ord[i].totprod)+" "+str(self.ord[i].lprod)+"\n")

    def openFile(self):
        with open('entrada.txt','w')as entrada:
           
            filepath =filedialog.askopenfilename(initialdir="Desktop", title = "Open Layout", filetypes=(("Text files","*.txt"),("All files","*.*")))
            entrada.write(filepath+"\n")
            file = open(filepath, 'r')
            arq = file.read().splitlines()
            print("Arquivo lido")

            filepath2 =filedialog.askopenfilename(initialdir="Desktop", title = "Open Products", filetypes=(("Text files","*.txt"),("All files","*.*")))
            entrada.write(filepath2+"\n")
            file2 = open(filepath2, 'r')
            arq2 = file2.read().splitlines()
            print("Arquivo lido")

            filepath3 =filedialog.askopenfilename(initialdir="Desktop", title = "Open Order", filetypes=(("Text files","*.txt"),("All files","*.*")))
            entrada.write(filepath3+"\n")
            file3 = open(filepath3, 'r')
            arq3 = file3.read().splitlines()
            print("Arquivo lido")

        self.leitura(arq,arq2,arq3)
   
class Produto:
    def __init__(self):
        self.idprod=0
        self.qtdprod=0
class Ordem:
    def __init__(self):
        self.totprod=0
        self.lprod = []
        self.qtprod = []
        self.a = [0,0]
        self.posic = []