import networkx as nx
import glob
from collections import Counter
import matplotlib.pyplot as plt

#Define o padrão para localizar os arquivos GEXF na pasta atual
pattern = "*.gexf"
#Cria uma lista com os nomes dos arquivos GEXF na pasta atual
files = glob.glob("./basedados/anos/*.gexf")

def processar_grafo(arquivo):
    try:
        #Carregar o grafo a partir do arquivo GEXF
        g = nx.read_gexf(arquivo)

        #Densidade da rede
        densidade = nx.density(g)

        #Número de nós(vertices)
        num_nos = g.number_of_nodes()

        #Número de arestas
        num_arestas = g.number_of_edges()

        #Grau médio(média dos vizinhos)
        #Obs: Em redes não dirigidas(reciprocidade), média = 2*L/N
        grau_medio = sum(dict(g.degree()).values()) / num_nos

        #Distribuição do número de vizinhos
        distribuicao = Counter(dict(g.degree()).values())
         # Exibe as métricas
        print(f"Arquivo: {arquivo}")
        print(f"Densidade da rede: {densidade:.4f}")
        print(f"Número de nós: {num_nos}")
        print(f"Número de arestas: {num_arestas}")
        print(f"Grau médio: {grau_medio:.2f}")
        print(f"Distribuição do número de vizinhos:{distribuicao}")
        print("-" * 40)
        
        # Opcional: plot da distribuição do grau
        plt.figure()
        plt.bar(distribuicao.keys(), distribuicao.values(), color='skyblue')
        plt.xlabel('Grau (Número de Vizinhos)')
        plt.ylabel('Número de nós')
        plt.title(f'Distribuição de Grau - {arquivo}')
        plt.show()
        
    except Exception as e:
        print(f"Erro ao processar {arquivo}: {e}")

# Processa cada arquivo GEXF encontrado
for arquivo in files:
    processar_grafo(arquivo)