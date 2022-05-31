#import matplotlib.pyplot as plt
#import sympy as sp
#import numpy as np
from tkinter import filedialog



class Armazem:
    def __init__(self):
        self.totalpro=0
        self.totalord=0
        self.po=[Produto()]
        self.ord=[Ordem()]
        self.nome = ""
    def leitura(self,arq1,arq2,arq3):
        
        
        self.nex = int(arq1[20])
        self.ney = int(arq1[20])
        self.nez = int(arq1[20])
        
        self.nsx = int(arq1[20])
        self.nsy = int(arq1[20])
        self.nsz = int(arq1[20])

        e =arq1[1].split() 
        s =arq1[3].split() 
        v=arq1[12].split()
        self.prt = int(e[1])*2
        self.cel = int(s[1])*int(v[1])
        
        for i in range(self.prt):
            self.pa.append(Prateleira())
            for j in range(self.cel):
                self.pa[i].pra.append(Celula())

        c=21
        for i in range(self.prt):               
            for j in range(self.cel):
                inf = arq1[c].split()
                self.pa[i].pra[j].idcel= int(inf[0])                                     
                self.pa[i].pra[j].xcel= int(inf[1])            
                self.pa[i].pra[j].ycel= int(inf[2])           
                self.pa[i].pra[j].zcel= 0                                  
                c+=1
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
                self.ord[i].lprod.append(int(inf[1+j]))
            b+=1

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
        print(self.nex,self.ney)
        print(self.nsx,self.nsy)
        print(self.prt)
        print(self.cel)
        for i in range(self.prt):
            for j in range(self.cel):
                print(self.pa[i].pra[j].idcel,self.pa[i].pra[j].capcel,self.pa[i].pra[j].xcel,self.pa[i].pra[j].ycel)
        print(self.totalpro)
        for i in range(self.totalpro):
            print(self.po[i].idprod,self.po[i].qtdprod)
        print(self.totalord)
        for i in range(self.totalord):
            print(self.ord[i].totprod,self.ord[i].lprod)

    def openFile(self):
        filepath =filedialog.askopenfilename(initialdir="Desktop", title = "Open Layout", filetypes=(("Text files","*.txt"),("All files","*.*")))
        file = open(filepath, 'r')
        arq = file.read().splitlines()
        print("Arquivo lido")

        filepath2 =filedialog.askopenfilename(initialdir="Desktop", title = "Open Products", filetypes=(("Text files","*.txt"),("All files","*.*")))
        file2 = open(filepath2, 'r')
        arq2 = file2.read().splitlines()
        print("Arquivo lido")

        filepath3 =filedialog.askopenfilename(initialdir="Desktop", title = "Open Order", filetypes=(("Text files","*.txt"),("All files","*.*")))
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
        self.a = [0,0]
        self.posic = []