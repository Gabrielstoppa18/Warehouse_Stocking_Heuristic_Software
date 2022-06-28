from pyparsing import And
import entrada
import math
import numpy as np
import copy
import sys
from pickle import LIST
from pandas import DataFrame as pd
from pandas import ExcelWriter as ex


class Pos():
    def __init__(self):
        self.produto = 0
        self.quantidade = 0       
class SA():
    def __init__(self):
        self.car=self.Carro()
        self.x=0
        self.y=0
        self.x0=0
        self.y0=0
        #self.alpha = 0.95
        #self.iter=10
        #self.Tf = 1.0
        #self.T0 = 5.0
        self.arm= entrada.Armazem()
        #self.cel=[]
        self.SOL=[]
        self.Xb=[]
        self.xb=[]
        self.xxb = sys.maxsize
        self.xy = [0,0]
        self.order=[]
        self.maxcar=2
    class Carro:
        def __init__(self):
            self.capcesta=2
            self.numcestas=5
            self.cestas=[]
            self.carrinho=[]
            
    def arquivos(self):
        file=open('entrada.txt','r')
        arq = file.read().splitlines()
        try:
            filepath1=arq[0]
            filepath2=arq[1]
            filepath3=arq[2]

            file1 = open(filepath1, 'r')
            arq1 = file1.read().splitlines()

            file2 = open(filepath2, 'r')
            arq2 = file2.read().splitlines()

            file3 = open(filepath3, 'r')
            arq3 = file3.read().splitlines()

            self.arm.leitura(arq1,arq2,arq3)
        except:
            self.arm.openFile()

    def solInicial(self):
        for i in range(self.car.numcestas):
                self.car.carrinho.append(self.car.cestas)
        self.SOL=[]

        self.randomid1 = []
        for j in range(len(self.arm.loc)):
            for k in range(len(self.arm.loc[j])):
                self.randomid1.append((j+1,k+1))
        np.random.shuffle(self.randomid1)
        for i in range(self.arm.totalpro):
            self.SOL.append(self.randomid1[i])
        self.order=copy.deepcopy(self.arm.ordens)
       
    def imprimeSol(self,SOL,order):


        print('Layout solução: ',SOL)
        print('Lista de produtos: ',order)
    def imprimeOrd(self,order):
        print('Lista de produtos: ',order)

    def objetivo(self,SOL,order):

        #order: (produto,ordem)
        #SOL: {Produto: (nó,prateleira)}s

        # self.SOL = SOL
        objetivo=[]
        objt=0.0
        
        #Coleta primeiro produto
        i,j=order[0]
        a,b=SOL[i-1]

        objt += self.arm.dist[0][a]
        self.car.carrinho[j].append(i)
    
        for l in range(0,len(order)-1):
            o,p=order[l]
            a,b=self.SOL[o-1]

            k,s=order[l+1]
            c,d=SOL[k-1]
            if len(self.car.carrinho[p])==self.car.capcesta:
                objt += self.arm.dist[a][0]
                self.car.carrinho[p]=[]
                objt += self.arm.dist[0][c]
                
                self.car.carrinho[s].append(c)  
            else:
                self.car.carrinho[s].append(c) 
                objt += self.arm.dist[a][c]
            
        #Retorna para a entrada
        i=len(order)-1
        g,h=order[i]
        a,b=SOL[h-1]
            
        objt += self.arm.dist[a][0]

            
        objetivo.append(objt)

        return sum(objetivo)

    
    def sa(self):
        #self.rd = np.random.randint(0,2)
        
        self.alpha =0.90
        self.it = 5
        self.Tf = 1
        self.T0 = 5
        self.arquivos()
        self.solInicial()
        self.imprimeSol(self.SOL,self.order)
        valor=self.objetivo(self.SOL,self.order)
        print("Custo inicial:", valor)
        
        self.Xb = copy.deepcopy(self.SOL)
        self.orderB=copy.deepcopy(self.order)
        self.xxb=valor

        self.T = self.T0

        while self.T >= self.Tf:
            for i in range(self.it):
                #print('-----------------ITERAÇÃO------------------')
                xx,ord = self.SA2(self.SOL,self.order)
                Y = copy.deepcopy(self.SOL)
                
                rd = np.random.randint(0,1)
                # self.r = self.rd
                if rd == 0:
                    self.N1(Y)
                   
                elif rd == 1:
                    self.N2(Y)
                   
                elif rd == 2:
                    self.N3(Y)
                  
                yy,ordy = self.SA2(Y,ord)
                delta = yy-xx
                if delta <= 0:
                    self.SOL = copy.deepcopy(Y)
                    self.order=copy.deepcopy(ordy)
                    # self.SOL = self.Y
                    xx = yy
                else:
                    rr = (np.random.randint(0,100))/100
                    if rr < math.exp(-delta/self.T):
                        # self.SOL = self.Y
                        self.SOL = copy.deepcopy(Y)
                        self.order=copy.deepcopy(ordy)
                        xx = yy
                if xx < self.xxb:
                    # self.Xb = self.SOL
                    self.Xb = copy.deepcopy(self.SOL)
                    self.orderB=copy.deepcopy(self.order)
                    self.xxb = xx
            
            self.T=self.alpha*self.T
            #print("-Temperatura Atual:",self.T)
        print("-Solução Final do Problema:")
        self.imprimeSol(self.Xb,self.orderB)
        print("-Custo Total da solução:",self.xxb)
        #self.datatxt(self.xxb,self.Xb,self.orderB)
        return self.xxb

    def N1(self, SOL):
        # self.SOL = SOL
        i = np.random.randint(0,len(SOL)-1)
        
        j = np.random.randint(0,len(SOL)-1)

        cont =5
        while i == j and cont >=0:
            i = np.random.randint(0,len(SOL)-1)
            j = np.random.randint(0,len(SOL)-1)
            cont= cont-1
        
        aux = SOL[i]
        SOL[i]= SOL[j]
        SOL[j]= aux
        
        #print("N1")
    def N2(self,SOL):
        # self.SOL = SOL
        i = np.random.randint(0,len(SOL)-1)

        j = np.random.randint(0,len(SOL)-1)

        cont=5
        while i == j and cont >=0:
            i = np.random.randint(0,len(SOL)-1)

            j = np.random.randint(0,len(SOL)-1)
            cont=cont-1
        aux=SOL[i]
        SOL.pop(i)
        SOL.insert(j,aux)
        
        #self.SOL[self.j][self.jc].quantidade = 0
        #print("N2")
    def N3(self,SOL):
        # self.SOL = SOL
        i = np.random.randint(0,len(SOL))
        j =0
        A0= sys.maxsize

        if SOL[i] == 0:
            return
        k=i
        for l in range(self.arm.cel):
            A = self.dist(self.arm.nex, self.arm.ney, self.arm.pa[k].pra[l].xcel,self.arm.pa[k].pra[l].ycel)
            if SOL[k][l] == 0 and A < A0:
                A0 = A
                j = k
                jc = l
        # if self.SOL[self.j][self.jc] != 0:
        #     return
        # if self.SOL[self.j][self.jc] != 0 and self.SOL[self.i][self.ic] == 0:
        #     return
        SOL[j] = SOL[i]
        SOL[i]= 0

        #self.SOL[self.i][self.ic].quantidade = 0
        #print("N3")
    def SA2(self,arm,ord):
        alpha =0.90
        it = 5
        Tf = 1
        T0 = 5
        T=T0
        xxb=sys.maxsize
        while T >= Tf:
            for i in range(it):
                xx = self.objetivo(arm,ord)
                y = copy.deepcopy(ord)
                rd = np.random.randint(0,1)
                # self.r = self.rd
                if rd == 0:
                    self.N_1(y)
                   
                elif rd == 1:
                    self.N_2(y)
                   
                
                yy = self.objetivo(arm,y)
                #print('yy: ',yy)
                delta = yy-xx
                if delta <= 0:
                    ord= copy.deepcopy(y)
                    # self.SOL = self.Y
                    xx = yy
                else:
                    rr = (np.random.randint(0,100))/100
                    if rr < math.exp(-delta/T):
                        # self.SOL = self.Y
                        ord = copy.deepcopy(y)
                        xx = yy
                if xx < xxb:
                    # self.Xb = self.SOL
                    xb = copy.deepcopy(ord)
                    xxb = xx
            
            T=alpha*T
            #print("-Temperatura Atual:",self.T)
        '''
        print("-Solução do SA2:")
        
        '''
        
        #self.imprimeSol(arm,xb)
        #print("-Custo solução SA2:",xxb)
        
        return xxb,xb
    def N_1(self,order):

        ii = np.random.randint(0,len(order)-1)
        jj = np.random.randint(0,len(order)-1)
        cont=5
        while ii==jj and cont >=0:
            ii = np.random.randint(0,len(order)-1)
            jj = np.random.randint(0,len(order)-1)
            cont=cont-1
        #print(ii,jj)
        aux = order[ii]
        order[ii]= order[jj]
        order[jj]= aux

    def N_2(self,order):

        ii = np.random.randint(0,len(order)-1)
        jj = np.random.randint(0,len(order)-1)
        cont=5
        while ii==jj and cont >=0:
            ii = np.random.randint(0,len(order)-1)
            jj = np.random.randint(0,len(order)-1)
            cont=cont-1
        #print(ii,jj)
        aux = order[ii]
        order.pop(order[ii])
        order.insert(order[jj],aux)
    
    def save_xls(self):
        df1 = pd({'Collect Orders': self.orderB})
        df2 = pd({'Warehouse': self.Xb})

        # Usando o ExcelWriter, cria um doc .xlsx, usando engine='xlsxwriter'
        writer = ex('Solution.xlsx', engine='xlsxwriter')

        # Armazena cada df em uma planilha diferente do mesmo arquivo
        df1.to_excel(writer, sheet_name='Collect Orders',index=False)
        df2.to_excel(writer, sheet_name='Layout Warehouse',index=False)

        # Fecha o ExcelWriter e gera o arquivo .xlsx
        writer.save()
        print("Solucao salva!")