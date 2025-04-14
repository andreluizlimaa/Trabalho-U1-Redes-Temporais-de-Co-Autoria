import networkx as nx
import glob
import math
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import joypy
import matplotlib.cm as cm

# -------------------------------------------------------------------
# Parte 1: Coleta das métricas individuais de cada arquivo GEXF
# -------------------------------------------------------------------
files = glob.glob("./basedados/anos/*.gexf")
files.sort()

anos = []
for f in files:
    nome = f.split('/')[-1]
    try:
        ano = int(nome[:4])
    except Exception:
        ano = None
    anos.append(ano)

if None in anos or len(anos) != len(files):
    anos = list(range(2010, 2010 + len(files)))

densidade = []
num_nos = []
num_arestas = []
grau_medio = []
distribuicao = []

for arquivo in files:
    try:
        g = nx.read_gexf(arquivo)
        d = nx.density(g)
        nn = g.number_of_nodes()
        na = g.number_of_edges()
        gm = sum(dict(g.degree()).values()) / nn
        dt = Counter(dict(g.degree()).values())

        densidade.append(d)
        num_nos.append(nn)
        num_arestas.append(na)
        grau_medio.append(gm)
        distribuicao.append(dt)
        
    except Exception as e:
        print(f"Erro ao processar {arquivo}: {e}")

print("Resumo das métricas:")
for d, nn, na, gm, dt in zip(densidade, num_nos, num_arestas, grau_medio, distribuicao):
    print(f"  Densidade: {d:.4f}")
    print(f"  Número de nós: {nn}")
    print(f"  Número de arestas: {na}")
    print(f"  Grau médio: {gm:.2f}")
    print(f"  Distribuição dos graus: {dt}")
    print("-" * 40)

# -------------------------------------------------------------------
# Parte 2: Criação do DataFrame com os graus dos nós por ano
# -------------------------------------------------------------------
degree_records = []

for arquivo, ano in zip(files, anos):
    try:
        g = nx.read_gexf(arquivo)
        deg_list = list(dict(g.degree()).values())
        nn = g.number_of_nodes()
        na = g.number_of_edges()
        for deg in deg_list:
            degree_records.append({
                'ano': ano,
                'degree': deg,
                'num_nos': nn,
                'num_arestas': na
            })
    except Exception as e:
        print(f"Erro ao processar {arquivo}: {e}")

df_degrees = pd.DataFrame(degree_records)
df_degrees = df_degrees.sort_values(by='ano')

# -------------------------------------------------------------------
# Parte 3: Gráficos
# -------------------------------------------------------------------

# Gráfico 1: Métricas ao longo dos anos
fig1 = plt.figure(figsize=(10, 6))
plt.plot(anos, densidade, marker='o', label='Densidade')
plt.plot(anos, num_nos, marker='o', label='Número de Nós')
plt.plot(anos, num_arestas, marker='o', label='Número de Arestas')
plt.plot(anos, grau_medio, marker='o', label='Grau Médio')

# Marcação de anos importantes referentes à avaliação do PPgEEC
marcos = [2012, 2016, 2020, 2024]
for marco in marcos:
    plt.axvline(x=marco, color='gray', linestyle='--', linewidth=1,
                label=f'PPgEEC {marco}' if marco == marcos[0] else "")  # adiciona label apenas para um item para evitar duplicata
    # Adiciona anotação do marco no topo do gráfico
    plt.text(marco, plt.ylim()[1]*0.46, f'{marco}', verticalalignment='top', color='gray')

plt.xticks(list(range(2010, 2025)))
plt.xlabel('Ano')
plt.ylabel('Valor')
plt.title('Métricas dos Grafos ao Longo dos Arquivos')
plt.legend()
plt.tight_layout()


# Gráfico 2: Ridgeline chart com joypy
fig2, axes = joypy.joyplot(
    data=df_degrees,
    by="ano",
    column="degree",
    figsize=(12, 8),
    kind="kde",
    overlap=1,
    colormap=cm.viridis,
    linecolor="black"
)

plt.xlabel("Grau (Número de Vizinhos)")
plt.title("Ridgeline Chart da Distribuição dos Graus por Ano\n(Coloração baseada no Número de Vértices)", y=0.90)

# Exibe ambos os gráficos juntos
plt.show()

# Fecha ambos para evitar que reabram
plt.close(fig1)
plt.close(fig2)
