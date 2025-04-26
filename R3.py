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
    # Arestas
    nx.draw_networkx_edges(rede_geral, pos=pos,
                        edge_color='black',
                        width=0.5,
                        alpha=0.5)
    # Nós
    nx.draw_networkx_nodes(rede_geral, pos=pos,
                        node_color="#1C8394",
                        node_size=20,
                        alpha=0.6,
                        edgecolors='#1C8394',
                        linewidths=0.5)
    
    # Labels (não exibido para não poluir)
    plt.title("Rede Geral (2010-2025)", fontsize=12)

    # Plotando o sub-grafo
    plt.subplot(1, 2, 2)
    # Arestas
    nx.draw_networkx_edges(subgrafo, pos=pos,
                           edge_color='black',
                           width=0.8,
                           alpha=0.7)
    # Nós
    nx.draw_networkx_nodes(subgrafo, pos=pos,
                        node_color="#390D02",
                        node_size=40,
                        alpha=0.9, 
                        edgecolors='#A52502',
                        linewidths=0.8)
    
    # Labels (também oculto)
    plt.title("Sub-Grafo (vértices com grau >= 80), X = 24", fontsize=12)
    
    plt.tight_layout()
    plt.show()


# =============================================================================
# PASSO 6: Analisar a rede ego de um vértice escolhido
# =============================================================================

def analisar_rede_ego(rede_geral: nx.Graph, no_escolhido=None):
    import matplotlib.pyplot as plt
    import networkx as nx

    if no_escolhido is None:
        no_escolhido = max(rede_geral.degree, key=lambda x: x[1])[0]

    ego = nx.ego_graph(rede_geral, no_escolhido)

    pos = nx.spring_layout(ego, seed=42)

    # Define cores e tamanhos
    node_colors = []
    node_sizes = []
    for node in ego.nodes():
        if node == no_escolhido:
            node_colors.append('#FFA500')
            node_sizes.append(600)
        else:
            node_colors.append('#1C8394')
            grau = ego.degree[node]
            node_sizes.append(100 + grau * 20)

    # Desenha as arestas
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_edges(ego, pos,
                           edge_color='black',
                           width=1.5,
                           alpha=0.7)

    # Desenha os nós
    nx.draw_networkx_nodes(ego, pos,
                           node_color=node_colors,
                           alpha=0.8,
                           node_size=node_sizes,
                           edgecolors='black',
                           linewidths=1.5)
    
    plt.title(f"Rede Ego do Vertice: {no_escolhido}", fontsize=16)
    plt.axis('off')
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
    analisar_rede_ego(rede_geral, no_escolhido="57214422700")
    
    
if __name__ == "__main__":
    main_expanded()
