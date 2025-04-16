import networkx as nx
import glob
import math
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import joypy
import matplotlib.cm as cm

# ===================================================================
# FUNÇÃO: coletar_arquivos_gexf
# Descrição: Coleta os caminhos dos arquivos GEXF em uma pasta e extrai
#            os anos dos arquivos (assumindo que o ano está nos 4 primeiros dígitos).
# ===================================================================
def coletar_arquivos_gexf(pasta: str):
    # Busca todos os arquivos .gexf na pasta especificada
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
    
    # Se algum ano não foi extraído ou a quantidade de anos não corresponde
    # à quantidade de arquivos, atribuímos anos sequenciais como padrão
    if None in anos or len(anos) != len(arquivos):
        anos = list(range(2010, 2010 + len(arquivos)))
    
    return arquivos, anos

# ===================================================================
# FUNÇÃO: calcular_metricas_grafo
# Descrição: Lê um arquivo GEXF, calcula as métricas do grafo (densidade,
#            número de nós, número de arestas, grau médio e distribuição dos graus)
# ===================================================================
def calcular_metricas_grafo(arquivo: str):
    try:
        grafo = nx.read_gexf(arquivo)
        densidade = nx.density(grafo)
        num_nos = grafo.number_of_nodes()
        num_arestas = grafo.number_of_edges()
        grau_medio = sum(dict(grafo.degree()).values()) / num_nos
        
        # Conta a distribuição dos graus usando Counter
        distribuicao_graus = Counter(dict(grafo.degree()).values())
        
        return {
            'densidade': densidade,
            'num_nos': num_nos,
            'num_arestas': num_arestas,
            'grau_medio': grau_medio,
            'distribuicao': distribuicao_graus
        }
    except Exception as e:
        print(f"Erro ao processar {arquivo}: {e}")
        return None

# ===================================================================
# FUNÇÃO: processar_metricas
# Descrição: Itera sobre os arquivos, calcula as métricas individuais e 
#            imprime um resumo.
# ===================================================================
def processar_metricas(arquivos: list):
    metricas_por_ano = []
    # Listas para armazenar as métricas de cada arquivo
    densidades = []
    nos = []
    arestas = []
    graus_medios = []
    distribuicoes = []
    
    for arquivo in arquivos:
        metrica = calcular_metricas_grafo(arquivo)
        if metrica:
            densidades.append(metrica['densidade'])
            nos.append(metrica['num_nos'])
            arestas.append(metrica['num_arestas'])
            graus_medios.append(metrica['grau_medio'])
            distribuicoes.append(metrica['distribuicao'])
            metricas_por_ano.append(metrica)
    
    # Exibe um resumo das métricas
    print("Resumo das métricas:")
    for d, n, a, gm, dist in zip(densidades, nos, arestas, graus_medios, distribuicoes):
        print(f"  Densidade: {d:.4f}")
        print(f"  Número de nós: {n}")
        print(f"  Número de arestas: {a}")
        print(f"  Grau médio: {gm:.2f}")
        print(f"  Distribuição dos graus: {dist}")
        print("-" * 40)
    
    return densidades, nos, arestas, graus_medios, distribuicoes

# ===================================================================
# FUNÇÃO: criar_dataframe_graus
# Descrição: Cria um DataFrame com os graus de cada nó, associando-os ao ano
#            correspondente e armazenando também o número total de nós e arestas.
# ===================================================================
def criar_dataframe_graus(arquivos: list, anos: list):
    registros_graus = []
    for arquivo, ano in zip(arquivos, anos):
        try:
            grafo = nx.read_gexf(arquivo)
            # Lista com os graus de cada nó
            lista_graus = list(dict(grafo.degree()).values())
            num_nos = grafo.number_of_nodes()
            num_arestas = grafo.number_of_edges()
            for grau in lista_graus:
                registros_graus.append({
                    'ano': ano,
                    'degree': grau,
                    'num_nos': num_nos,
                    'num_arestas': num_arestas
                })
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")
            
    df = pd.DataFrame(registros_graus)
    df = df.sort_values(by='ano')
    return df

# ===================================================================
# FUNÇÃO: plotar_metricas_temporais
# Descrição: Plota as métricas calculadas (densidade, número de nós, número de arestas,
#            grau médio) ao longo dos anos, incluindo marcações de anos de avaliação.
# ===================================================================
def plotar_metricas_temporais(anos: list, densidades: list, nos: list, arestas: list, graus_medios: list):
    fig = plt.figure(figsize=(10, 6))
    plt.plot(anos, densidades, marker='o', label='Densidade')
    plt.plot(anos, nos, marker='o', label='Número de Nós')
    plt.plot(anos, arestas, marker='o', label='Número de Arestas')
    plt.plot(anos, graus_medios, marker='o', label='Grau Médio')
    
    # Define marcos importantes referentes à avaliação do PPgEEC
    marcos = [2012, 2016, 2020, 2024]
    for i, marco in enumerate(marcos):
        plt.axvline(x=marco, color='gray', linestyle='--', linewidth=1,
                    label=f'PPgEEC {marco}' if i == 0 else "")
        # Adiciona anotação do marco no topo do gráfico
        plt.text(marco, plt.ylim()[1]*0.46, f'{marco}', verticalalignment='top', color='gray')
    
    plt.xticks(list(range(2010, 2025)))
    plt.xlabel('Ano')
    plt.ylabel('Valor')
    plt.title('Métricas dos Grafos ao Longo dos anos')
    plt.legend()
    plt.tight_layout()
    return fig

# ===================================================================
# FUNÇÃO: plotar_ridgeline
# Descrição: Plota um gráfico ridgeline utilizando joypy para visualizar a distribuição
#            dos graus dos nós por ano.
# ===================================================================
def plotar_ridgeline(df_degrees: pd.DataFrame):
    fig, axes = joypy.joyplot(
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
    return fig

# ===================================================================
# MAIN: Execução do script
# ===================================================================
def main():
    # Etapa 1: Coleta de arquivos e definição dos anos
    pasta_arquivos = "./basedados/anos"
    arquivos, anos = coletar_arquivos_gexf(pasta_arquivos)
    
    # Etapa 2: Processamento das métricas dos grafos
    densidades, nos, arestas, graus_medios, distribuicoes = processar_metricas(arquivos)
    
    # Etapa 3: Criação do DataFrame com graus dos nós por ano
    df_degrees = criar_dataframe_graus(arquivos, anos)
    
    # Etapa 4: Plotagem dos gráficos
    fig1 = plotar_metricas_temporais(anos, densidades, nos, arestas, graus_medios)
    fig2 = plotar_ridgeline(df_degrees)
    
    # Exibe os gráficos
    plt.show()
    
    # Fecha as figuras para evitar reabertura desnecessária
    plt.close(fig1)
    plt.close(fig2)

# Executa a função main se o script for executado diretamente
if __name__ == "__main__":
    main()
