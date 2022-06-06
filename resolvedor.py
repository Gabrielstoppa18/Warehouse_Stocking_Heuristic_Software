from pyparsing import And
import entrada
import math
import numpy as np
import copy
import sys

class Pos():
    def __init__(self):
        self.produto = 0
        self.quantidade = 0       
class SA():
    def __init__(self):
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
        
    def solInicial(self):
        # self.SOL=SOL 

        self.SOL=[]
        '''
        for a in range(self.arm.totalLocations):
            self.SOL.append(self.cel)
        '''
        self.randomid1 = []
        for j in range(len(self.arm.loc)):
            for k in range(len(self.arm.loc[j])):
                self.randomid1.append((j+1,k+1))
        np.random.shuffle(self.randomid1)
        for i in range(self.arm.totalpro):
            self.SOL.append(self.randomid1[i])
        self.order=copy.deepcopy(self.arm.ord)
        '''
        #self.randomid = np.arange(self.arm.totalpro)
        np.random.shuffle(self.randomid1)
        self.randomid2 = []
        for i in range((self.arm.totalLocations)-self.arm.totalpro):
            self.randomid2.append(0)
        self.arr=self.randomid1+self.randomid2
        self.randomid=np.array(self.arr)
        #self.randomid=self.randomid.reshape(self.arm.numAisles,self.arm.numLocPerAisleSide*2*self.arm.numShelves)
        
        self.SOL=copy.deepcopy(self.randomid)
             
       
        self.posics=[]
        self.nodes=[]
        #inicialisa posics
        for i in range(self.arm.totalLocations):
            self.posics.append(0)
        #inicialisa nodes
        for i in range(self.arm.totalpro):
            self.nodes.append(0)
        #posics posicao+1: celula/ valor: no
        for i in range(self.arm.totalLocations):
            for j in range(len(self.arm.loc)):
                for k in range(len(self.arm.loc[j])):
                    if i+1==self.arm.loc[j][k]:
                        self.posics[i]=j+1
        #print(self.posics)
        for i in range(len(self.posics)):
            if i ==self.arm.totalpro:
                break
            self.nodes[self.SOL[i]-1]=self.posics[i]
        print(self.nodes)
        '''
    def imprimeSol(self,SOL,order):
        # self.SOL = SOL

        print('Layout solução: ',SOL)
        for l in range(self.arm.totalord):
            print('Ordem: ',l+1)
            print('Lista de produtos: ',order[l].lprod)
    # def iniciaPosic(self):
    #     for cont in range(self.arm.totalord):
    #         self.arm.ord[cont].posic.append(self.arm.ord[cont].a)

    def imprimeOrd(self,order):
        for l in range(self.arm.totalord):
            print('Ordem: ',l+1)
            print('Lista de produtos: ',order[l].lprod)

    def objetivo(self,SOL,order):
        # self.SOL = SOL
        objetivo=[]
         
        for l in range(self.arm.totalord):
            objt=0.0
            capcar=0
            j=order[l].lprod[0]
            a,b=SOL[j-1]
            capcar+=1
            objt += self.arm.dist[0][a]
            for i in range(len(order[l].lprod)-1):
                j=order[l].lprod[i]
                a,b=self.SOL[j-1]

                k=order[l].lprod[i+1]
                c,d=SOL[k-1]
                if capcar==self.maxcar:
                   objt += self.arm.dist[a][0]
                   objt += self.arm.dist[0][c]
                   capcar=0
                   
                else:
                    capcar+=1 
                    objt += self.arm.dist[a][c]

            i=len(order[l].lprod)
            j=order[l].lprod[i-1]
            a,b=SOL[j-1]
            
            
            objt += self.arm.dist[a][0]
            capcar=0
            objetivo.append(objt)
        '''
        for a in range(self.arm.totalpro):
            for j in range(len(self.nodes)):
                if a ==
        for l in range(len(order)):
            posics.append(list_)
            for i in range(len(order[l].lprod)):
                for j in range(len(self.nodes)):
                    if order[l].lprod[i]==j+1:
                        posics[l].append(self.nodes[j])
                
        print(posics) 

        
        objt= 0.0
        for j in range(len(posics)):
            for i in range(len(posics[j])):
                if i == 0: #primeiro
                    objt += self.arm.dist[0][posics[j][i]]
                elif i + 1 == len(posics): #ultimo produto
                        objt += self.arm.dist[posics[j][i]][0]
                else: #produto intermediario na lista
                        objt += self.arm.dist[posics[j][i]][posics[j][i+1]]
            objetivo.append(objt)
        '''   
        return sum(objetivo)

    
    def sa(self):
        #self.rd = np.random.randint(0,2)
        
        self.alpha =0.90
        self.it = 5
        self.Tf = 1
        self.T0 = 5
        
        self.solInicial()
        self.imprimeSol(self.SOL,self.order)
        valor=self.objetivo(self.SOL,self.order)
        print("Custos:", valor)
        
        self.Xb = copy.deepcopy(self.SOL)
        self.orderB=copy.deepcopy(self.order)
        self.xxb=valor

        self.T = self.T0

        while self.T >= self.Tf:
            for i in range(self.it):
                print('-----------------ITERAÇÃO------------------')
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
                print('yy: ',yy)
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
        
        self.imprimeSol(arm,xb)
        print("-Custo solução SA2:",xxb)
        
        return xxb,xb
    def N_1(self,order):

        i = np.random.randint(0,self.arm.totalord-1)
        #j = np.random.randint(0,self.arm.totalord-1)
        while len(order[i].lprod) <=1:
            i = np.random.randint(0,self.arm.totalord-1)
        ii = np.random.randint(0,len(order[i].lprod)-1)
        jj = np.random.randint(0,len(order[i].lprod)-1)
        cont=5
        while ii==jj and cont >=0:
            ii = np.random.randint(0,len(order[i].lprod)-1)
            jj = np.random.randint(0,len(order[i].lprod)-1)
            cont=cont-1
        print(i,ii,jj)
        aux = order[i].lprod[ii]
        order[i].lprod[ii]= order[i].lprod[jj]
        order[i].lprod[jj]= aux

    def N_2(self,order):

        i = np.random.randint(0,self.arm.totalord-1)
        #j = np.random.randint(0,self.arm.totalord-1)
        while len(order[i].lprod) <=1:
            i = np.random.randint(0,self.arm.totalord-1)
        ii = np.random.randint(0,len(order[i].lprod)-1)
        jj = np.random.randint(0,len(order[i].lprod)-1)
        cont=5
        while ii==jj and cont >=0:
            ii = np.random.randint(0,len(order[i].lprod)-1)
            jj = np.random.randint(0,len(order[i].lprod)-1)
            cont=cont-1
        print(i,ii,jj)
        aux = order[i].lprod[ii]
        order[i].lprod.pop(order[i].lprod[ii])
        order[i].lprod.insert(order[i].lprod[jj],aux)