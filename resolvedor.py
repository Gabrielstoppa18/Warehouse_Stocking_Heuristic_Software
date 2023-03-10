from pyparsing import And
import entrada_o
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
        self.cestas= self.Cesta()
        self.car=self.Carro()
        self.x=0
        self.y=0
        self.x0=0
        self.y0=0
        #self.alpha = 0.95
        #self.iter=10
        #self.Tf = 1.0
        #self.T0 = 5.0
        self.arm= entrada_o.Armazem()
        #self.cel=[]
        self.SOL=[]
        self.Xb=[]
        self.xb=[]
        self.xxb = sys.maxsize
        self.xy = [0,0]
        self.order=[]
        self.pos_ordem=[]
        self.maxcar=2
        self.close=[]
    class Carro:
        def __init__(self):
            self.capcesta=0
            self.numcestas=0
            self.captotal=self.capcesta*self.numcestas
            self.carrinho=[]
    class Cesta:
        def __init__(self):
            self.produtos=[]
            self.ordem=0

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
        self.SOL=[]
        self.order=[]
        self.pos_ordem=[]

        self.car.capcesta=self.arm.capcesta
        self.car.numcestas=self.arm.numcestas
        for i in range(self.arm.totalord):
            self.pos_ordem.append(-1)
        for i in range(self.car.numcestas):
                self.car.carrinho.append(self.cestas)
        self.SOL=[]

        self.randomid1 = []
        for j in range(len(self.arm.loc)):
            for k in range(len(self.arm.loc[j])):
                self.randomid1.append((j+1,k+1))
        np.random.shuffle(self.randomid1)
        for i in range(self.arm.totalpro):
            self.SOL.append(self.randomid1[i])
        self.order=copy.deepcopy(self.arm.ordens)

        for i in range(1,self.arm.numProdVertices):
            self.close.append((self.arm.dist[0][i],i))
        #print(sorted(self.close))
       
    def imprimeSol(self,SOL,order):


        print('Layout solução: ',SOL)
        print('Lista de produtos: ',order)
    def imprimeOrd(self,order):
        print('Lista de produtos: ',order)

    def organizar(self,order):

        for i in range(len(order)):
            o,p,u=order[i]
            for j in range(i+1,len(order)):
                k,s,v=order[j]
                if o==k:
                    aux=order[j]
                    order.pop(j)
                    order.insert(i+1,aux)
    
    def cesta_vazia(self,pos_ordem):
        for i in range(len(pos_ordem)):
            if pos_ordem[i][1] < self.car.capcesta:
                return pos_ordem[i][0]
                    
    def objetivo2(self,SOL,ordem):
        order=copy.deepcopy(ordem)
        '''
        print("Ordem antes",order)
        
        print("Ordem depois",order)
        '''
        #order: (produto,ordem)
        #SOL: {Produto: (nó,prateleira)}s
        for i in range(len(self.pos_ordem)):
            self.pos_ordem[i]=[]
        objt=0.0
        cesta_usada=0
        #Coleta primeiro produto
        i,j,e=order[0]
        a,b=SOL[i-1]
        capcar=0
        objt += self.arm.dist[0][a]
        for k in range(e):
            self.pos_ordem[j].append((cesta_usada,0))
            cesta_usada+=1
        id= self.cesta_vazia(self.pos_ordem[j])
        self.car.carrinho[id].produtos.append(i)
        capcar+=1
        l=1

        prod_pos_atual=a
        order[0][0]=-1
        while True:
            if l >= len(order):
                #a,b=self.SOL[prod_pos_atual-1]
                a=prod_pos_atual
                objt += self.arm.dist[a][0]
                for i in range(len(self.car.carrinho)):
                    self.car.carrinho[i].produtos=[]
                    
                for i in range(len(self.pos_ordem)):
                    self.pos_ordem[i]=[]
                cesta_usada=0
                l=-1
                for i in range(len(order)):
                    if order[i][0] != -1:
                        l=i 
                        break
                #print(l)
                prod_pos_atual=0
                if l==-1:
                    break
            #o,p,u=order[pos_atual]
            a=prod_pos_atual
            '''if len(self.pos_ordem[p]) > 0:
                u=self.cesta_vazia(self.pos_ordem[j])               
            else:
                if cesta_usada+ u <=self.car.numcestas:
                    for k in range(u):
                        self.pos_ordem[p].append((cesta_usada,0))
                        cesta_usada+=1
                else:
                    print("Erro 1:", l)
                    l+=1
                    continue'''
            k,s,v=order[l]
            
            if k==-1:
                l+=1
                continue
            c,d=SOL[k-1]
            if len(self.pos_ordem[s]) > 0:
                v=self.cesta_vazia(self.pos_ordem[s])
            else:
                if cesta_usada+ v <=self.car.numcestas:
                    for k in range(v):
                        self.pos_ordem[s].append((cesta_usada,0))
                        cesta_usada+=1
                    v=self.cesta_vazia(self.pos_ordem[s])
                else:
                    #print("Erro 2:", l)
                    l+=1
                    continue
            objt += self.arm.dist[a][c]
            self.car.carrinho[v].produtos.append(c)
            capcar+=1

            prod_pos_atual=c
            order[l][0]=-1
            l+=1

            '''if  len(self.car.carrinho[v].produtos) == self.car.capcesta:
                if cesta_usada>=self.car.numcestas:
                    pass
                else:
                    self.pos_ordem[s].append(cesta_usada)
                    cesta_usada+=1 
            if cesta_usada>=self.car.numcestas:
                objt += self.arm.dist[a][0]
                for i in range(len(self.car.carrinho)):
                    self.car.carrinho[i].produtos=[]
                objt += self.arm.dist[0][c]

                self.car.carrinho[v].produtos.append(c)
                for j in range(len(self.pos_ordem)):
                    self.pos_ordem[j]=[]
                cesta_usada=0
                self.pos_ordem[s].append(cesta_usada)
                cesta_usada+=1
                capcar+=1
                order.pop(l)  
            else:
                objt += self.arm.dist[a][c]
                self.car.carrinho[v].produtos.append(c)
                capcar+=1
                order.pop(l)
                if  len(self.car.carrinho[v].produtos) == self.car.capcesta:
                    if cesta_usada>=self.car.numcestas:
                        pass
                    else:
                        self.pos_ordem[s].append(cesta_usada)
                        cesta_usada+=1 '''
                
        #Retorna para a entrada
        
        return objt


    def objetivo(self,SOL,ordem):
        order=copy.deepcopy(ordem)
        '''
        print("Ordem antes",order)
        
        print("Ordem depois",order)
        '''
        #order: (produto,ordem)
        #SOL: {Produto: (nó,prateleira)}s
        for i in range(len(self.pos_ordem)):
            self.pos_ordem[i]=-1
        objetivo=[]
        objt=0.0
        cesta_usada=0
        #Coleta primeiro produto
        i,j,e=order[0]
        a,b=SOL[i-1]
        capcar=0
        objt += self.arm.dist[0][a]
        self.pos_ordem[j]=cesta_usada
        cesta_usada+=1
        self.car.carrinho[self.pos_ordem[j]].produtos.append(i)
        capcar+=1
        l=0
        while len(order)!=1:
            o,p,u=order[l]
            a,b=self.SOL[o-1]
            if self.pos_ordem[p] != -1:
                u=self.pos_ordem[p]
            else:
                self.pos_ordem[p]=cesta_usada
                cesta_usada+=1
            k,s,v=order[l+1]
            c,d=SOL[k-1]

            if self.pos_ordem[s] != -1:
                v=self.pos_ordem[s]
            else:
                self.pos_ordem[s]=cesta_usada
                cesta_usada+=1

            if cesta_usada>=self.car.numcestas:
                objt += self.arm.dist[a][0]
                for i in range(len(self.car.carrinho)):
                    self.car.carrinho[i].produtos=[]
                objt += self.arm.dist[0][c]

                self.car.carrinho[v].produtos.append(c)
                for j in range(len(self.pos_ordem)):
                    self.pos_ordem[j]=-1
                cesta_usada=0
                self.pos_ordem[s]=cesta_usada
                cesta_usada+=1
                capcar+=1
                order.pop(l)  
            else:
                objt += self.arm.dist[a][c]
                self.car.carrinho[v].produtos.append(c)
                capcar+=1
                order.pop(l) 
                
        #Retorna para a entrada
        i=len(order)-1
        g,h,v=order[i]
        a,b=SOL[h-1]
            
        objt += self.arm.dist[a][0]

            
        objetivo.append(objt)

        return sum(objetivo)

    
    def sa(self):
                
        self.alpha =0.95
        self.it = 10
        self.Tf = 1
        self.T0 = 5
        #self.arquivos()
        del self.SOL
        del self.order
        self.SOL=[]
        self.order=[]
        self.pos_ordem=[]
        self.solInicial()
        #self.imprimeSol(self.SOL,self.order)
        valor=self.objetivo2(self.SOL,self.order)
 
        self.organizar(self.order)


        print("Custo inicial:", valor)
        
        self.Xb = copy.deepcopy(self.SOL)
        self.orderB=copy.deepcopy(self.order)
        self.xxb=valor

        self.T = self.T0
        xx,ord = self.SA2(self.SOL,self.order)
        '''while self.T >= self.Tf:
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
        #self.imprimeSol(self.Xb,self.orderB)
        print("-Custo Total da solução:",self.xxb)'''
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
        for s in range(len(SOL)):
            for i in range(len(self.order)):
                k,j,e=self.order[i] 
                #if
       
    def SA2(self,arm,ord):
        alpha =0.90
        it = 1000
        Tf = 1
        T0 = 10
        T=T0

        ####Contando os operadores####
        n1=0
        n2=0
        n3=0
        n4=0
        ##############################

        #####Parametros RL#####
        al=0.1#alpha
        gamma=0.1
        epsilon=0.1
        epsilon_decay=0.99#fator de decaimento
        #######################
        
        dict_Q={}
        xxb=sys.maxsize
        while T >= Tf:
            for i in range(it):
                reward=0
                epsilon=epsilon*epsilon_decay#decaimento
                xx = self.objetivo2(arm,ord)
                y = copy.deepcopy(ord)
                ys=str(y)
                if np.random.rand()<epsilon:
                    #print("Aleatório")
                    rd = np.random.randint(0,4)
                else:
                    if ys in dict_Q:
                        r=dict_Q[ys]
                        if r[1]<=0:
                            #print("IA")
                            rd = np.random.randint(0,4)
                        else:
                            #print("Sem dados")
                            rd=r[0]

                    else:
                        rd = np.random.randint(0,4)  

                #print(rd)
                # self.r = self.rd
                if rd == 0:
                    self.N_1(y)
                    n1+=1

                elif rd == 1:
                    self.N_2(y)
                    n2+=1

                elif rd == 2:
                    self.N_3(y)
                    n3+=1
                elif rd == 3:
                    self.N_4(y)
                    n4+=1

                self.organizar(y)
                yy = self.objetivo2(arm,y)
                #print('yy: ',yy)
                delta = yy-xx
                if delta <= 0:
                    ord= copy.deepcopy(y)
                    reward=10
                    # self.SOL = self.Y
                    xx = yy
                else:
                    reward=-5
                    rr = (np.random.randint(0,100))/100
                    if rr < math.exp(-delta/T):
                        # self.SOL = self.Y
                        ord = copy.deepcopy(y)
                        xx = yy
                if xx < xxb:
                    reward=15
                    # self.Xb = self.SOL
                    xb = copy.deepcopy(ord)
                    xxb = xx

                #######RL######
                #Q.append(y_current),rd,reward
                dict_Q[ys]=[rd,reward]
            T=alpha*T
            #print("-Temperatura Atual:",self.T)
        '''
        print("-Solução do SA2:")
        
        '''
        print("N1: ",n1)
        print("N2: ",n2)
        print("N3: ",n3)
        print("N4: ",n4)
        #self.imprimeSol(arm,xb)
        print("-Custo solução SA2:",xxb)
        
        return xxb,xb
    def N_1(self,order):

        ##operador troca##

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

        ##operador inserção##

        ii = np.random.randint(0,len(order)-1)
        jj = np.random.randint(0,len(order)-1)
        cont=5
        while ii==jj and cont >=0:
            ii = np.random.randint(0,len(order)-1)
            jj = np.random.randint(0,len(order)-1)
            cont=cont-1
        
        aux = order[ii]
        order.pop(ii)
        order.insert(jj,aux)

    def N_3(self,lista):

        ##operador permutação##

        i = np.random.randint(0,len(lista)-1)
        j = np.random.randint(0,len(lista)-1)
        cont=5
        while i==j and cont >=0:
            i = np.random.randint(0,len(lista)-1)
            j = np.random.randint(0,len(lista)-1)
            cont=cont-1
        sublista = lista[i:j]
        np.random.shuffle(sublista)
        lista[i:j] = sublista

    def N_4(self,lista):

        ##operador inversão##

        i = np.random.randint(0,len(lista)-1)
        j = np.random.randint(0,len(lista)-1)
        cont=5
        while i==j and cont >=0:
            i = np.random.randint(0,len(lista)-1)
            j = np.random.randint(0,len(lista)-1)
            cont=cont-1
        lista[i:j] = reversed(lista[i:j])      

    def save_xls(self):
        produtos=np.arange(1,len(self.Xb)+1)
        print(len(produtos))
        nos=[]
        prateleira=[]
        for j in range(len(self.Xb)):
            a,b=self.Xb[j]
            nos.append(a)
            prateleira.append(b)
        print(len(nos))
        print(len(prateleira))
        produto_o=[]
        ordem=[]
        for i in range(len(self.orderB)):
            a,b,c=self.orderB[i]
            produto_o.append(a)
            ordem=b
        df1 = pd({'Products': produto_o,'Order': ordem})
        df2 = pd({'Products': produtos,'Nodes': nos,'Shelves': prateleira})

        # Usando o ExcelWriter, cria um doc .xlsx, usando engine='xlsxwriter'
        #writer = ex('Solution.xlsx')
        writer = ex('Solution.xlsx', engine='xlsxwriter')
        # Armazena cada df em uma planilha diferente do mesmo arquivo
        df1.to_excel(writer, sheet_name='Collect Orders',index=False)
        df2.to_excel(writer, sheet_name='Layout Warehouse',index=False)

        # Fecha o ExcelWriter e gera o arquivo .xlsx
        writer.save()
        print("Solucao salva!")