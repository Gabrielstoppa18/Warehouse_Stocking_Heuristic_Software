def organize_coleta(ordem_de_coleta):
    # Ordenar a lista de acordo com a ordem do produto
    ordem_de_coleta.sort(key=lambda x: x[1])
    
    carrinhos = [[] for _ in range(3)]  # Inicialização dos carrinhos vazios
    cesta_capacidade = 10
    cestas_por_carrinho = 8
    produtos_por_cesta = []  # Lista para controlar a quantidade de produtos em cada cesta
    
    for ordem in ordem_de_coleta:
        id_produto, ordem_produto, qtd_cestas = ordem
        
        # Verificar se há espaço na cesta atual do carrinho da ordem
        carrinho_atual = ordem_produto % 3
        cesta_atual = len(produtos_por_cesta) % cestas_por_carrinho
        
        if cesta_atual >= cestas_por_carrinho:
            carrinho_atual = (carrinho_atual + 1) % 3
            cesta_atual = 0
        
        # Verificar se é necessário começar uma nova cesta no carrinho atual
        if produtos_por_cesta and (produtos_por_cesta[-1] % cesta_capacidade) + qtd_cestas * cesta_capacidade > cesta_capacidade:
            cesta_atual = (cesta_atual + 1) % cestas_por_carrinho
        
        produtos_por_cesta.extend([qtd_cestas * cesta_capacidade] * cesta_capacidade)
        
        # Adicionar o produto ao carrinho e à cesta correspondente
        carrinhos[carrinho_atual].append(id_produto)
        
    return carrinhos

# # Ordem de coleta fornecida pelo usuário
# ordem_de_coleta = [(52, 0, 2), (119, 0, 2), (271, 0, 2), (308, 0, 2), (381, 0, 2), (472, 0, 2), (501, 0, 2), (622, 0, 2), (646, 0, 2), (722, 0, 2), (1116, 
# 0, 2), (1128, 0, 2), (1144, 0, 2), (1188, 0, 2), (1196, 0, 2), (1299, 0, 2), (1322, 0, 2), (1470, 0, 2), (47, 1, 2), (113, 1, 2), (253, 1, 2), (403, 1, 2), (497, 1, 2), 
# (563, 1, 2), (923, 1, 2), (979, 1, 2), (1090, 1, 2), (1173, 1, 2), (1395, 1, 2), (16, 2, 2), (531, 2, 2), (741, 2, 2), (848, 2, 2), (1040, 2, 2), (1048, 2, 2), (1058, 2, 2), (1090, 2, 2), (1125, 2, 2), (1190, 2, 2), (1264, 2, 2), (15, 3, 2), (27, 3, 2), (48, 3, 2), (431, 3, 2), (454, 3, 2), (524, 3, 2), (840, 3, 2), (1163, 3, 2), (1196, 3, 2), (1223, 3, 2), (1340, 3, 2), (395, 4, 1), (717, 4, 1), (751, 4, 1), (927, 4, 1), (934, 4, 1), (1227, 4, 1), (1277, 4, 1), (1377, 4, 1)]

# carrinhos_organizados = organize_coleta(ordem_de_coleta)
# print(carrinhos_organizados)

for i in range(1, 11):
    command = f"nohup python3 script_d20_{i}.py > saida_d20_{i}.txt 2> erro_d20_{i}.txt &"
    print(command)