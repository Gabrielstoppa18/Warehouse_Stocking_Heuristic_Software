from pyparsing import And
import entrada_o
import math
import numpy as np
import copy
import sys
from pickle import LIST
from pandas import DataFrame as df
from pandas import ExcelWriter as ex
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from joblib import Parallel, delayed
import time




np.set_printoptions(threshold=np.inf)

class Pos():
    def __init__(self):
        self.produto = 0
        self.quantidade = 0       
class SA():
    def __init__(self):
        
        self.cesta= self.Cesta()
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

        num_cestas = 8
        capacidade_cesta = 10
        self.num_tipos=self.arm.totalord
        self.carrinho = self.Carrinho(num_cestas, capacidade_cesta,self.num_tipos)
        
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
        self.sclose=[]
        self.prod_score=[]
    class Carrinho:
        def __init__(self, num_cestas, capacidade_cesta,num_tipos):
            self.num_cestas = num_cestas
            self.capacidade_cesta = capacidade_cesta
            self.cestas = {tipo: [] for tipo in range(0, num_tipos)}
            self.coletado = {tipo: [] for tipo in range(0, num_tipos)}
            self.distancia_total = 0
    
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
    def clear(self):
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
        self.sclose=[]
        self.prod_score=[]
    def solInicial(self):
        #self.clear()
        for i in range(self.arm.totalpro):
            self.SOL.append(0)
        self.order=[]
        self.pos_ordem=[]
        self.sclose=[]

        self.car.capcesta=self.arm.capcesta
        self.car.numcestas=self.arm.numcestas
        for i in range(self.arm.totalord):
            self.pos_ordem.append(-1)
        for i in range(self.car.numcestas):
            self.car.carrinho.append(self.cesta)
        
        '''
        
        np.random.shuffle(self.randomid1)
        for i in range(self.arm.totalpro):
            self.SOL.append(self.randomid1[i])
        
        '''
        self.order=copy.deepcopy(self.arm.ordens)

        self.randomid1 = []
        for j in range(len(self.arm.loc)):
            for k in range(len(self.arm.loc[j])):
                self.randomid1.append((j+1,k+1))

        for i in range(1,self.arm.numProdVertices+1):
            self.close.append((self.arm.dist[0][i],i))
            self.sclose=sorted(self.close,key=lambda x: x[0])
        
        self.n_close=[]
        for i in range(len(self.sclose)):
            a,b=self.sclose[i]
            for j in range(1,7):
                self.n_close.append((b,j))

        for i in range(self.arm.totalpro):
            a,b=self.prod_score[i]
            self.SOL[a-1]=self.n_close[i]
            
        num_cestas = 8
        capacidade_cesta = 10
        self.num_tipos=self.arm.totalord
        self.carrinho = self.Carrinho(num_cestas, capacidade_cesta,self.num_tipos)
        
    
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
                    
    def objetivo4(self,SOL,ordem):
        distancia_total=0
        order=copy.deepcopy(ordem)
        old=0
        for i in range(len(order)):
            o,p,u=order[i]
            a,b=self.SOL[o-1]
            posicao=a
            tipo = p
            distancia_total += self.arm.dist[old][a]
            
            if len(self.carrinho.cestas[tipo]) >= self.carrinho.capacidade_cesta:
                # Se a cesta estiver cheia, vá para a próxima cesta
                cesta_cheia = True
                
                for i in range(0, self.carrinho.num_cestas+1):
                    
                    if len(self.carrinho.cestas[i]) < self.carrinho.capacidade_cesta:
                        # Se houver uma cesta vazia, use-a
                        cesta_cheia = False
                        self.carrinho.cestas[i].append(posicao)
                        break
                    
                if cesta_cheia:
                    # Se todas as cestas estiverem cheias, volte ao início
                    print("encheu todas")
                    distancia_total += self.arm.dist[a][0]
                    self.carrinho.cestas = {tipo: [] for tipo in range(0, self.num_tipos)}
                    self.carrinho.cestas[tipo].append(posicao)
            else:
                self.carrinho.cestas[tipo].append(posicao)
            self.carrinho.coletado[tipo].append(posicao)
            old=a
            
        # Depois de visitar todos os locais, volte ao início
        i=order[-1]
        o,p,u=i
        a,b=self.SOL[o-1]
        distancia_total += self.arm.dist[a][0]
        self.carrinho.cestas = {tipo: [] for tipo in range(0, self.num_tipos)}
        return(distancia_total)

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

        #Retorna para a entrada
        
        return objt

    def objetivo3(self,SOL,ordem):
        order=copy.deepcopy(ordem)
        objetivo=[]
        objt=0.0

        #Coleta primeiro produto
        i,j,e=order[0]
        a,b=SOL[i-1]
        objt += self.arm.dist[0][a]
        l=0

        while len(order)!=1:

            o,p,u=order[l]
            a,b=self.SOL[o-1]
            k,s,v=order[l+1]
            c,d=SOL[k-1]
            objt += self.arm.dist[a][c]
            order.pop(l)

        #Retorna para a entrada
        i=len(order)-1
        g,h,v=order[i]
        a,b=SOL[h-1]
            
        objt += self.arm.dist[a][0]    
        objetivo.append(objt)

        return sum(objetivo)


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

    def ml(self,trim):
        #self.prod_score=[]
        dados = pd.read_csv('dados.csv')
        tri=str(trim) #1,2 ou 3

        # Dividir dados em conjunto de treinamento e teste
        x = dados.drop(['Produtos', tri], axis=1)
        y = dados[tri]
        x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size=0.2)

        # Treinar modelo
        modelo = RandomForestRegressor(n_estimators=100, random_state=0)
        modelo.fit(x_treino, y_treino)

        # Avaliar modelo
        y_pred = modelo.predict(x_teste)
        erro = abs(y_pred - y_teste)
        #print('Erro médio:', round(erro.mean(), 2))

        # Fazer previsões
        y_novo = modelo.predict(x)
        for i in range(len(y_novo)):
            self.prod_score.append((i+1,y_novo[i]))
        self.prod_score=sorted(self.prod_score, key=lambda x: x[1],reverse=True)
        #print('Produtos mais vendidos:', y_novo)

    def sa(self):
        start_time = time.time()
        self.ml(1)    
        self.alpha =0.95
        self.it = 5
        self.Tf = 1
        self.T0 = 10
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
        self.xxb=xx
        while self.T >= self.Tf:

            for i in range(self.it):
                #print('-----------------ITERAÇÃO------------------')
                xx,ord = self.SA2(self.SOL,self.order)
                Y = copy.deepcopy(self.SOL)
                
                rd = np.random.randint(1,5)
                # self.r = self.rd
                if rd == 1:
                    self.N1(Y)
                   
                elif rd == 2:
                    self.N2(Y)
                   
                elif rd == 3:
                    self.N3(Y)
               
                elif rd == 4:
                    self.N4(Y)
                  
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
        print("-Custo Total da solução:",self.xxb)
        #self.datatxt(self.xxb,self.Xb,self.orderB)
        end_time = time.time()
        time_seq = end_time - start_time
        print(f"Tempo de execucao do SA: {time_seq:.4f} segundos")
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
    def N3(self,lista):

        ##operador permutação##

        i = np.random.randint(0,self.tamam-1)
        j = np.random.randint(0,self.tamam-1)
        cont=5
        while i==j and cont >=0:
            i = np.random.randint(0,self.tamam-1)
            j = np.random.randint(0,self.tamam-1)
            cont=cont-1
        sublista = lista[i:j]
        np.random.shuffle(sublista)
        lista[i:j] = sublista

    def N4(self,lista):

        ##operador inversão##

        i = np.random.randint(0,self.tamam-1)
        j = np.random.randint(0,self.tamam-1)
        cont=5
        while i==j and cont >=0:
            i = np.random.randint(0,self.tamam-1)
            j = np.random.randint(0,self.tamam-1)
            cont=cont-1
        lista[i:j] = reversed(lista[i:j])   
    

    def SA2(self,arm,ord):
        start_time = time.time()
        self.tamam=len(ord)
        alpha =0.95
        it = 1000
        Tf = 1
        T0 = 5
        T=T0
        self.armazem=arm
        self.ordemi=ord
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
        xb=[]
        dict_Q={}
        xxb=sys.maxsize
        while T >= Tf:

            '''
            total = [it]*4 # 4 elementos na lista para processar em paralelo
            results = Parallel(n_jobs=4)(delayed(self.for_SA2)(its,T0,dict_Q,ord,arm) for its in total)
            min_result = min(results, key=lambda x: x[0])
            xxb=min_result[0]
            xb=min_result[1]
            '''
            for i in range(it):
                reward=0
                epsilon=epsilon*epsilon_decay#decaimento
                xx = self.objetivo3(arm,ord)
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
                yy = self.objetivo3(arm,y)
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
                #'''
            T=alpha*T
            #print("-Temperatura Atual:",self.T)
        '''
        print("-Solução do SA2:")
        
        
        print("N1: ",n1)
        print("N2: ",n2)
        print("N3: ",n3)
        print("N4: ",n4)'''
        #self.imprimeSol(arm,xb)
        
        end_time = time.time()
        time_seq = end_time - start_time
        print(f"Tempo de execução SA2: {time_seq:.4f} segundos")
        print("-Custo solução SA2:",xxb)
        
        
        return xxb,xb
    def N_1(self,order):

        ##operador troca##

        ii = np.random.randint(0,self.tamam-1)
        jj = np.random.randint(0,self.tamam-1)
        cont=5
        while ii==jj and cont >=0:
            ii = np.random.randint(0,self.tamam-1)
            jj = np.random.randint(0,self.tamam-1)
            cont=cont-1
        #print(ii,jj)
        aux = order[ii]
        order[ii]= order[jj]
        order[jj]= aux

    def N_2(self,order):

        ##operador inserção##

        ii = np.random.randint(0,self.tamam-1)
        jj = np.random.randint(0,self.tamam-1)
        cont=5
        while ii==jj and cont >=0:
            ii = np.random.randint(0,self.tamam-1)
            jj = np.random.randint(0,self.tamam-1)
            cont=cont-1
        
        aux = order[ii]
        order.pop(ii)
        order.insert(jj,aux)

    def N_3(self,lista):

        ##operador permutação##

        i = np.random.randint(0,self.tamam-1)
        j = np.random.randint(0,self.tamam-1)
        cont=5
        while i==j and cont >=0:
            i = np.random.randint(0,self.tamam-1)
            j = np.random.randint(0,self.tamam-1)
            cont=cont-1
        sublista = lista[i:j]
        np.random.shuffle(sublista)
        lista[i:j] = sublista

    def N_4(self,lista):

        ##operador inversão##

        i = np.random.randint(0,self.tamam-1)
        j = np.random.randint(0,self.tamam-1)
        cont=5
        while i==j and cont >=0:
            i = np.random.randint(0,self.tamam-1)
            j = np.random.randint(0,self.tamam-1)
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
        df1 = df({'Products': produto_o,'Order': ordem})
        df2 = df({'Products': produtos,'Nodes': nos,'Shelves': prateleira})

        # Usando o ExcelWriter, cria um doc .xlsx, usando engine='xlsxwriter'
        #writer = ex('Solution.xlsx')
        writer = ex('Solution.xlsx', engine='xlsxwriter')
        # Armazena cada df em uma planilha diferente do mesmo arquivo
        df1.to_excel(writer, sheet_name='Collect Orders',index=False)
        df2.to_excel(writer, sheet_name='Layout Warehouse',index=False)

        # Fecha o ExcelWriter e gera o arquivo .xlsx
        writer.save()
        print("Solucao salva!")
