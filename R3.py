import networkx as nx
import glob
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# FUNÇÃO: coletar_arquivos_gexf
# (Utilizada conforme o seu script para coletar os arquivos e extrair os anos.)
# =============================================================================
def coletar_arquivos_gexf(pasta: str):
    arquivos = glob.glob(f"{pasta}/*.gexf")
    arquivos.sort()
    anos = []
    for caminho in arquivos:
        nome_arquivo = caminho.split('/')[-1]
        try:
            ano = int(nome_arquivo[:4])
        except Exception:
            ano = None
        anos.append(ano)
    
    if None in anos or len(anos) != len(arquivos):
        anos = list(range(2010, 2010 + len(arquivos)))
    
    return arquivos, anos

# =============================================================================
# FUNÇÃO: ler_grafos
# Descrição: Lê cada arquivo GEXF e retorna a lista de grafos
# =============================================================================
def ler_grafos(arquivos: list):
    grafos = []
    for arquivo in arquivos:
        try:
            G = nx.read_gexf(arquivo)
            grafos.append(G)
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")
    return grafos

# =============================================================================
# PASSO 1: Gerar a rede geral (união dos grafos de 2010 a 2025)
# =============================================================================
def gerar_rede_geral(grafos: list):
    # Inicia com o primeiro grafo da lista
    rede_geral = grafos[0]
    # Une os demais grafos (a operação compose garante a união dos nós e arestas)
    for g in grafos[1:]:
        rede_geral = nx.compose(rede_geral, g)
    return rede_geral

# =============================================================================
# PASSO 2: Definir X (número mínimo de vizinhos)
# Metodologia: Utilizamos o percentil 80 da distribuição dos graus dos nós
# da rede geral. Dessa forma, focamos em nós com alta conectividade.
# =============================================================================
def definir_limite_minimo(rede_geral: nx.Graph, percentil=80):
    graus = [d for n, d in rede_geral.degree()]
    X = np.percentile(graus, percentil)
    # Como o grau é inteiro, arredondamos para o inteiro superior
    X = int(np.ceil(X))
    print(f"Definido X = {X} (Percentil {percentil} da distribuição dos graus)")
    return X

# =============================================================================
# PASSO 3: Gerar o sub-grafo com nós com grau >= X
# =============================================================================
def gerar_subgrafo(rede_geral: nx.Graph, X: int):
    # Filtra os nós que possuem grau >= X
    nos_filtrados = [n for n, d in rede_geral.degree() if d >= X]
    subgrafo = rede_geral.subgraph(nos_filtrados).copy()
    return subgrafo

# =============================================================================
# PASSO 4: Calcular e comparar a densidade dos grafos
# =============================================================================
def comparar_densidade(rede_geral: nx.Graph, subgrafo: nx.Graph):
    densidade_geral = nx.density(rede_geral)
    densidade_subgrafo = nx.density(subgrafo)
    print(f"Densidade da rede geral: {densidade_geral:.4f}")
    print(f"Densidade do sub-grafo: {densidade_subgrafo:.4f}")
    return densidade_geral, densidade_subgrafo

# =============================================================================
# PASSO 5: Visualizar a rede geral e o sub-grafo
# =============================================================================
def visualizar_grafos(rede_geral: nx.Graph, subgrafo: nx.Graph):
    # Utiliza o mesmo layout para facilitar comparação
    pos = nx.spring_layout(rede_geral, seed=42)  # fixa o seed para consistência
    plt.figure(figsize=(14, 6))
    
    # Plotando a rede geral
    plt.subplot(1, 2, 1)
    nx.draw_networkx(rede_geral, pos=pos, node_size=20, with_labels=False)
    plt.title("Rede Geral (2010-2025)")
    
    # Plotando o sub-grafo
    plt.subplot(1, 2, 2)
    nx.draw_networkx(subgrafo, pos=pos, node_size=40, with_labels=False)
    plt.title("Sub-Grafo (vértices com grau >= 80), X = 24")
    
    plt.tight_layout()
    plt.show()

# =============================================================================
# PASSO 6: Analisar a rede ego de um vértice escolhido
# =============================================================================
def analisar_rede_ego(rede_geral: nx.Graph, no_escolhido=None):
    # Se nenhum nodo for especificado, escolhe o de maior grau
    if no_escolhido is None:
        no_escolhido = max(rede_geral.degree, key=lambda x: x[1])[0]
    ego = nx.ego_graph(rede_geral, no_escolhido)
    
    # Calcula métricas básicas para a rede ego
    grau_nodo = rede_geral.degree[no_escolhido]
    densidade_ego = nx.density(ego)
    
    print(f"Nó escolhido: {no_escolhido}")
    print(f"Grau do nodo na rede geral: {grau_nodo}")
    print(f"Densidade da rede ego: {densidade_ego:.4f}")
    
    # Visualização da rede ego
    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(ego, seed=42)
    nx.draw_networkx(ego, pos=pos, node_color='lightgreen', node_size=300)
    plt.title(f"Rede Ego do vértice: {no_escolhido}")
    plt.show()
    
    return ego

# =============================================================================
# MAIN: Execução do script expandido
# =============================================================================
def main_expanded():
    # Caminho para os arquivos GEXF (assegure que o caminho está correto)
    pasta_arquivos = "./avaliacao_total"
    arquivos, anos = coletar_arquivos_gexf(pasta_arquivos)
    
    # Leitura dos grafos
    grafos = ler_grafos(arquivos)
    
    # Gerar a rede geral unindo os grafos
    rede_geral = gerar_rede_geral(grafos)
    print(f"Rede geral: {rede_geral.number_of_nodes()} nós, {rede_geral.number_of_edges()} arestas")
    
    # Definir valor de X com base no percentil 80 da distribuição de graus
    X = definir_limite_minimo(rede_geral, percentil=80)
    
    # Gerar sub-grafo com nós que possuem pelo menos X vizinhos
    subgrafo = gerar_subgrafo(rede_geral, X)
    print(f"Sub-grafo: {subgrafo.number_of_nodes()} nós, {subgrafo.number_of_edges()} arestas")
    
    # Comparar densidades
    comparar_densidade(rede_geral, subgrafo)
    
    # Visualizar as redes
    visualizar_grafos(rede_geral, subgrafo)
    
    # Analisar a rede ego de um vértice escolhido (o de maior grau por padrão)
    analisar_rede_ego(rede_geral)
    
    # INTERPRETAÇÃO DOS RESULTADOS:
    #
    # 1. **Definição de X:**  
    #    Ao definir X como o percentil 80 dos graus, estamos considerando que os vértices com 
    #    conectividade acima desse valor representam os nós “centrales” ou de alta influência.  
    #
    # 2. **Densidade:**  
    #    A comparação entre a densidade da rede geral e a do sub-grafo pode revelar se os nós 
    #    com alta conectividade formam um “core” bem interligado. Se a densidade do sub-grafo for 
    #    significativamente maior, isso indica que estes nós mantêm muitas conexões entre si, 
    #    formando um núcleo coeso.
    #
    # 3. **Visualização:**  
    #    Ao plotar as duas redes lado a lado, nota-se visualmente que o sub-grafo tende a ser mais 
    #    compacto e com maior interconectividade entre os nós destacados, em contraste com a rede
    #    geral que pode conter comunidades mais dispersas.
    #
    # 4. **Rede Ego:**  
    #    A análise da rede ego de um vértice (o de maior grau, por exemplo) nos revela a vizinhança 
    #    imediata deste nó e como seus vizinhos se conectam entre si. Uma alta densidade nessa rede 
    #    pode indicar que o nó está inserido em um cluster forte, potencialmente funcionando como 
    #    um hub que facilita a comunicação entre diferentes partes da rede.
    
if __name__ == "__main__":
    main_expanded()
