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
import time
import random

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
        self.dict_Q = {}
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
    def solInicial(self):
        #self.clear()
      
        self.SOL = [0] * self.arm.totalpro
        self.order = []
        self.pos_ordem = []
        self.sclose = []
    
        self.car.capcesta = self.arm.capcesta
        self.car.numcestas = self.arm.numcestas
        self.car.carrinho = [self.cesta] * self.car.numcestas
        self.pos_ordem = [-1] * self.arm.totalord
    
        self.order = copy.deepcopy(self.arm.ordens)
    
        self.randomid1 = [(j+1,k+1) for j in range(len(self.arm.loc)) for k in range(len(self.arm.loc[j]))]
        np.random.shuffle(self.randomid1)
    
        for i in range(1, self.arm.numProdVertices+1):
            self.close.append((self.arm.dist[0][i], i))
        self.sclose = sorted(self.close, key=lambda x: x[0])
        
        self.n_close = [(b, j) for i in range(len(self.sclose))
                       for b in (self.sclose[i][1],)
                       for j in range(1, 7)]
            
        for i, (a,b) in enumerate(self.prod_score):
            self.SOL[a-1] = self.n_close[i]
    
        num_cestas = 8
        capacidade_cesta = 10
        self.num_tipos = self.arm.totalord
        self.carrinho = self.Carrinho(num_cestas, capacidade_cesta, self.num_tipos)
    
    def organizar(self, order):
        for i, (o, p, u) in enumerate(order):
            for j in range(i+1, len(order)):
                k, s, v = order[j]
                if o == k:
                    order.pop(j)
                    order.insert(i+1, (k, s, v))
    
    
    def cesta_vazia(self, pos_ordem):
        for ordem in pos_ordem:
            produto, quantidade = ordem
            if quantidade < self.car.capcesta:
                return produto

    def objetivo2(self, SOL, ordem):
        order = [(i-1, j, e) for i, j, e in ordem]
        # Clearing self.pos_ordem using the * operator
        self.pos_ordem = [[] for _ in range(len(self.pos_ordem))] 
        objt = 0.0
        cesta_usada = 0
        #Coleta primeiro produto
        i, j, e = order[0]
        a, b = SOL[i]
        capcar = 0
        objt += self.arm.dist[0][a]

        # Using * operator and extend to add (cesta_usada,0) e times to self.pos_ordem[j]
        self.pos_ordem[j].extend([(cesta_usada, 0)] * e)
        id = self.cesta_vazia(self.pos_ordem[j])
        self.car.carrinho[id].produtos = [i]
        capcar += 1
        l = 1

        prod_pos_atual = a
        order[0] = (-1, j, e)
        while True:
            if l >= len(order):
                a = prod_pos_atual
                objt += self.arm.dist[a][0]
                # Using a for loop to clear the .produtos attribute of each cart
                for cart in self.car.carrinho:
                    cart.produtos = []
                # Using the * operator to clear self.pos_ordem
                self.pos_ordem = [[] for _ in range(len(self.pos_ordem))]
                cesta_usada = 0
                l = -1
                i = 0
                while i < len(order) and order[i][0] == -1:
                    order[i] = (-1, *order[i][1:])
                    i += 1
                prod_pos_atual = 0
                if i >= len(order):
                    break
                l = i
            a = prod_pos_atual
            k, s, v = order[l]
            if k == -1:
                l += 1
                continue
            c, d = SOL[k]
            if self.pos_ordem[s]:
                v = self.cesta_vazia(self.pos_ordem[s])
            else:
                if cesta_usada + v <= self.car.numcestas:
                    self.pos_ordem[s].extend([(cesta_usada, 0)] * v)
                    cesta_usada += v
                    v = self.cesta_vazia(self.pos_ordem[s])
                else:
                    l += 1
                    continue
            objt += self.arm.dist[a][c]
            self.car.carrinho[v].produtos.append(c)
            capcar += 1
    
            prod_pos_atual = c
            order[l] = (-1, s, v)
            l += 1
    
        return objt

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
        self.ml(3)    
        self.alpha = 0.95
        self.it = 5
        self.Tf = 1
        self.T0 = 10
        self.SOL = []
        self.order = []
        self.pos_ordem = []
        self.solInicial()
        valor = self.objetivo2(self.SOL, self.order)
        self.organizar(self.order)
    
        print("Custo inicial:", valor)
            
        self.Xb = copy.deepcopy(self.SOL)
        self.orderB = copy.deepcopy(self.order)
        self.xxb = valor
    
        self.T = self.T0
        xx, ord = self.SA2(self.SOL, self.order)
        self.xxb = xx
        while self.T >= self.Tf:
            for i in range(self.it):
                #print('-----------------ITERAÇÃO------------------')
                Y = copy.deepcopy(self.SOL)
                rd = np.random.randint(1, 5)

                if rd == 1:
                    self.N1(Y)
                elif rd == 2:
                    self.N2(Y)
                elif rd == 3:
                    self.N3(Y)
                elif rd == 4:
                    self.N4(Y)

                yy, ordy = self.SA2(Y, ord)
                delta = yy - xx
                if delta <= 0 or np.random.rand() < math.exp(-delta / self.T):
                    self.SOL, xx, ord = Y, yy, ordy
                if xx < self.xxb:
                    self.Xb, self.xxb, self.orderB = copy.deepcopy(self.SOL), xx, copy.deepcopy(ord)
    
            self.T *= self.alpha
            #print("-Temperatura Atual:",self.T)
    
        print("-Solução Final do Problema:")
        print("-Custo Total da solução:", self.xxb)
        end_time = time.time()
        time_seq = end_time - start_time
        print(f"Tempo de execucao do SA: {time_seq:.4f} segundos")
        return self.xxb
    

    def N1(self, SOL):
        i, j = np.random.choice(len(SOL), 2, replace=False)
        SOL[i], SOL[j] = SOL[j], SOL[i]
        #print("N1")

    def N2(self, SOL):
        i, j = np.random.choice(len(SOL), 2, replace=False)
        SOL[i], SOL[j] = SOL[j], SOL[i]
    
    def N3(self, lista):
        i, j = np.random.choice(len(lista), 2, replace=False)
        if i > j:
            i, j = j, i
        lista[i:j] = reversed(lista[i:j])
    

    def N4(self, lista):
        i, j = np.random.choice(len(lista), 2, replace=False)
        if i > j:
            i, j = j, i
        lista[i:j] = lista[i:j][::-1]

    def SA2(self, arm, ord):
        self.tamam=len(ord)
        start_time = time.time()
        tamam = len(ord)
        alpha = 0.90
        it = 1000
        Tf = 1
        T0 = 5
        T = T0
        armazem = arm
        ordemi = ord
        n1 = n2 = n3 = n4 = 0
        al = gamma = epsilon = 0.1
        epsilon_decay = 0.99
        
        xxb = sys.maxsize
        dict_t={}
        while T >= Tf:
            for i in range(it):
                reward = 0
                epsilon *= epsilon_decay
                xx = self.objetivo2(arm, ord)
                y = ord.copy()
                ys = str(y)
                arms=str(arm)
                if random.random() < epsilon:
                    rd = random.randint(0, 3)
                else:
                    if arms in self.dict_Q and ys in self.dict_Q[arms] and self.dict_Q[arms][ys][1] > 0:
                        rd = self.dict_Q[arms][ys][0]
                    else:
                        rd = random.randint(0, 3)

                if rd == 0:
                    self.N_1(y)
                    n1 += 1
                elif rd == 1:
                    self.N_2(y)
                    n2 += 1
                elif rd == 2:
                    self.N_3(y)
                    n3 += 1
                elif rd==3:
                    self.N_4(y)
                    n4 += 1
        
                self.organizar(y)
                yy = self.objetivo2(arm, y)
                delta = yy - xx
        
                if delta <= 0:
                    ord = y.copy()
                    reward = 10
                    xx = yy
                else:
                    reward = -5
                    if random.random() < np.exp(-delta / T):
                        ord = y.copy()
                        xx = yy
        
                if xx < xxb:
                    xb = y.copy()
                    xxb = xx
                    reward = 15
                dict_t[ys]=[rd, reward]
                self.dict_Q[arms]=dict_t
        
            T *= alpha
        
        end_time = time.time()
        time_seq = end_time - start_time
        print(f"Tempo de execução SA2: {time_seq:.4f} segundos")
        print("-Custo solução SA2:", xxb)
        
        return xxb, xb
   
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