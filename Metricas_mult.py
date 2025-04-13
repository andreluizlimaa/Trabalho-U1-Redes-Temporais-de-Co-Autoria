import networkx as nx
import glob
import math
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# Define o padrão para localizar os arquivos GEXF na pasta desejada
files = glob.glob("./basedados/anos/*.gexf")
files.sort()  # Ordena os arquivos (ex.: cronologicamente se os nomes permitirem)

# Listas para armazenar as métricas de cada arquivo
densidade = []
num_nos = []
num_arestas = []
grau_medio = []
distribuicao = []

# Processa cada arquivo e armazena as métricas
for arquivo in files:
    try:
        # Carrega o grafo a partir do arquivo GEXF
        g = nx.read_gexf(arquivo)

        # Calcula as métricas
        d = nx.density(g)                           # Densidade da rede
        nn = g.number_of_nodes()                      # Número de nós (vértices)
        na = g.number_of_edges()                      # Número de arestas
        gm = sum(dict(g.degree()).values()) / nn      # Grau médio (soma dos graus / número de nós)
        dt = Counter(dict(g.degree()).values())       # Distribuição do número de vizinhos

        # Armazena cada métrica em uma lista individual
        densidade.append(d)
        num_nos.append(nn)
        num_arestas.append(na)
        grau_medio.append(gm)
        distribuicao.append(dt)
        
    except Exception as e:
        print(f"Erro ao processar {arquivo}: {e}")

# Imprime no console um resumo com todas as métricas utilizando descompactação da tupla
print("Resumo das métricas:")
for d, nn, na, gm, dt in zip(densidade, num_nos, num_arestas, grau_medio, distribuicao):
    print(f"  Densidade: {d:.4f}")
    print(f"  Número de nós: {nn}")
    print(f"  Número de arestas: {na}")
    print(f"  Grau médio: {gm:.2f}")
    print(f"  Distribuição dos graus: {dt}")
    print("-" * 40)

# Se desejar gerar 4 curvas (densidade, vértices, arestas e grau médio) em um único gráfico,
# você pode usar o matplotlib. Exemplo simples:

plt.figure(figsize=(10, 6))
indices = range(len(files))

plt.plot(indices, densidade, marker='o', label='Densidade')
plt.plot(indices, num_nos, marker='o', label='Número de Nós')
plt.plot(indices, num_arestas, marker='o', label='Número de Arestas')
plt.plot(indices, grau_medio, marker='o', label='Grau Médio')

plt.xlabel('Arquivo (ordem cronológica)')
plt.ylabel('Valor')
plt.title('Métricas dos Grafos ao Longo dos Arquivos')
plt.legend()
plt.tight_layout()
plt.show()
