import networkx as nx
import glob
import matplotlib.pyplot as plt
import numpy as np
import os

# =============================================================================
# FUNÇÃO: coletar_arquivos_gexf
# (Utilizada para coletar os arquivos e extrair os anos.)
# =============================================================================
def coletar_arquivos_gexf(pasta: str):
    arquivos = glob.glob(f"{pasta}/*.gexf")
    arquivos.sort()
    anos = []
    for caminho in arquivos:
        nome_arquivo = os.path.basename(caminho)  # Solução mais robusta para extrair o nome
        try:
            ano = int(nome_arquivo[:4])
        except ValueError:
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
    
    if not grafos:
        raise ValueError("Nenhum grafo foi carregado. Verifique o caminho dos arquivos.")
    
    return grafos

# =============================================================================
# PASSO 1: Gerar a rede geral (união dos grafos de 2010 a 2025)
# =============================================================================
def gerar_rede_geral(grafos: list):
    if not grafos:
        raise ValueError("Lista de grafos vazia.")
    
    # Inicia com o primeiro grafo da lista
    rede_geral = grafos[0].copy()  # Criamos uma cópia para não modificar o original
    
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
    if rede_geral.number_of_nodes() == 0:
        raise ValueError("Rede vazia. Não é possível calcular o limite mínimo.")
    
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
    
    if not nos_filtrados:
        print(f"Aviso: Nenhum nó com grau >= {X} encontrado.")
        return nx.Graph()
    
    subgrafo = rede_geral.subgraph(nos_filtrados).copy()
    return subgrafo

# =============================================================================
# PASSO 4: Calcular e comparar a densidade dos grafos
# =============================================================================
def comparar_densidade(rede_geral: nx.Graph, subgrafo: nx.Graph):
    densidade_geral = nx.density(rede_geral)
    
    if subgrafo.number_of_nodes() <= 1:
        densidade_subgrafo = 0
        print("Aviso: Subgrafo possui 1 ou 0 nós, densidade definida como 0.")
    else:
        densidade_subgrafo = nx.density(subgrafo)
    
    print(f"Densidade da rede geral: {densidade_geral:.6f}")
    print(f"Densidade do sub-grafo: {densidade_subgrafo:.6f}")
    
    if densidade_subgrafo > densidade_geral:
        print(f"O subgrafo é {densidade_subgrafo/densidade_geral:.2f} vezes mais denso que a rede geral.")
    elif densidade_geral > 0:
        print(f"A rede geral é {densidade_geral/densidade_subgrafo:.2f} vezes mais densa que o subgrafo.")
    
    return densidade_geral, densidade_subgrafo

# =============================================================================
# PASSO 5: Visualizar a rede geral e o sub-grafo
# =============================================================================
def visualizar_grafos(rede_geral: nx.Graph, subgrafo: nx.Graph):
    if rede_geral.number_of_nodes() == 0:
        print("Aviso: Rede geral vazia. Visualização cancelada.")
        return
    
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
    
    plt.title(f"Rede Geral (2010-2025)\n{rede_geral.number_of_nodes()} nós, {rede_geral.number_of_edges()} arestas", fontsize=12)
    plt.axis('off')
    
    # Plotando o sub-grafo
    plt.subplot(1, 2, 2)
    
    if subgrafo.number_of_nodes() > 0:
        # Arestas
        nx.draw_networkx_edges(subgrafo, pos={node: pos[node] for node in subgrafo.nodes() if node in pos},
                            edge_color='black',
                            width=0.8,
                            alpha=0.7)
        # Nós
        nx.draw_networkx_nodes(subgrafo, pos={node: pos[node] for node in subgrafo.nodes() if node in pos},
                            node_color="#390D02",
                            node_size=40,
                            alpha=0.9, 
                            edgecolors='#A52502',
                            linewidths=0.8)
        
        plt.title(f"Sub-Grafo (vértices com grau >= X)\n{subgrafo.number_of_nodes()} nós, {subgrafo.number_of_edges()} arestas", fontsize=12)
    else:
        plt.text(0.5, 0.5, "Subgrafo vazio", fontsize=14, ha='center')
        plt.title("Sub-Grafo (vértices com grau >= X)", fontsize=12)
    
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("comparacao_grafos.png", dpi=300, bbox_inches='tight')
    plt.show()

# =============================================================================
# PASSO 6: Analisar a rede ego de um vértice escolhido
# =============================================================================
def analisar_rede_ego(rede_geral: nx.Graph, no_escolhido=None, raio=1):
    if rede_geral.number_of_nodes() == 0:
        print("Aviso: Rede vazia. Impossível analisar rede ego.")
        return None
    
    # Se nenhum nó for escolhido, seleciona o de maior grau
    if no_escolhido is None or no_escolhido not in rede_geral.nodes():
        if rede_geral.number_of_nodes() > 0:
            no_escolhido = max(rede_geral.degree, key=lambda x: x[1])[0]
            print(f"Nó escolhido automaticamente: {no_escolhido} (maior grau)")
        else:
            print("Erro: Rede não possui nós.")
            return None
    
    # Gera a rede ego com o raio especificado
    ego = nx.ego_graph(rede_geral, no_escolhido, radius=raio)
    
    print(f"Análise da rede ego do vértice {no_escolhido}:")
    print(f"- Número de vizinhos (1º nível): {len(list(rede_geral.neighbors(no_escolhido)))}")
    print(f"- Tamanho total da rede ego (raio {raio}): {ego.number_of_nodes()} nós")
    print(f"- Densidade da rede ego: {nx.density(ego):.6f}")
    
    # Coeficiente de clustering
    try:
        clustering = nx.clustering(ego, no_escolhido)
        print(f"- Coeficiente de clustering: {clustering:.6f}")
    except:
        print("- Não foi possível calcular o coeficiente de clustering")
    
    # Visualização
    pos = nx.spring_layout(ego, seed=42)
    
    # Define cores e tamanhos
    node_colors = []
    node_sizes = []
    for node in ego.nodes():
        if node == no_escolhido:
            node_colors.append('#FFA500')  # Laranja para o nó central
            node_sizes.append(600)
        else:
            node_colors.append('#1C8394')  # Azul para os vizinhos
            grau = ego.degree[node]
            node_sizes.append(100 + grau * 10)  # Tamanho proporcional ao grau
    
    # Desenha as arestas e nós
    plt.figure(figsize=(10, 10))
    nx.draw_networkx_edges(ego, pos, edge_color='black', width=1.0, alpha=0.7)
    nx.draw_networkx_nodes(ego, pos, 
                          node_color=node_colors,
                          alpha=0.8,
                          node_size=node_sizes,
                          edgecolors='black',
                          linewidths=1.5)
    
    plt.title(f"Rede Ego do Vértice: {no_escolhido} (raio={raio})", fontsize=16)
    plt.axis('off')
    plt.savefig(f"rede_ego_{no_escolhido}.png", dpi=300, bbox_inches='tight')
    plt.show()
    
    return ego

# =============================================================================
# MAIN: Execução do script expandido
# =============================================================================
def main_expanded():
    # Caminho para os arquivos GEXF
    pasta_arquivos = "./avaliacao_total"
    print(f"Buscando arquivos em: {pasta_arquivos}")
    
    try:
        # Coleta e leitura dos grafos
        arquivos, anos = coletar_arquivos_gexf(pasta_arquivos)
        print(f"Encontrados {len(arquivos)} arquivos GEXF")
        
        if not arquivos:
            print("Nenhum arquivo GEXF encontrado. Verifique o caminho.")
            return
        
        grafos = ler_grafos(arquivos)
        print(f"Carregados {len(grafos)} grafos")
        
        # Gerar a rede geral unindo os grafos
        rede_geral = gerar_rede_geral(grafos)
        print(f"Rede geral: {rede_geral.number_of_nodes()} nós, {rede_geral.number_of_edges()} arestas")
        
        # Definir valor de X com base no percentil 80 da distribuição de graus
        X = definir_limite_minimo(rede_geral, percentil=80)
        
        # Gerar sub-grafo com nós que possuem pelo menos X vizinhos
        subgrafo = gerar_subgrafo(rede_geral, X)
        print(f"Sub-grafo: {subgrafo.number_of_nodes()} nós, {subgrafo.number_of_edges()} arestas")
        
        # Comparar densidades
        densidade_geral, densidade_subgrafo = comparar_densidade(rede_geral, subgrafo)
        
        # Visualizar as redes
        visualizar_grafos(rede_geral, subgrafo)
        
        # Configurar o ID do vértice para analisar a rede ego
        # Mantemos o vértice escolhido pelo usuário, mas com verificação de existência
        vertice_escolhido = "57214422700"
        if vertice_escolhido not in rede_geral.nodes():
            print(f"Vértice {vertice_escolhido} não encontrado. Usando o de maior grau.")
            vertice_escolhido = None
        
        # Analisar a rede ego do vértice escolhido
        ego = analisar_rede_ego(rede_geral, no_escolhido=vertice_escolhido, raio=1)
        
        print("\nAnálise de rede concluída com sucesso!")
    
    except Exception as e:
        import traceback
        print(f"Erro durante a execução: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main_expanded()