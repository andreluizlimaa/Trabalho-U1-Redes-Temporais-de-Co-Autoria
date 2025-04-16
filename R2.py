import networkx as nx
import matplotlib.pyplot as plt
import os

periodos = ["2010-2012", "2013-2016", "2017-2020", "2021-2024"]
caminho_arquivos = "./basedados/avaliacao_geral"

def visualizar_rede_por_periodo(arquivo_gexf, periodo):
    try:
        G = nx.read_gexf(arquivo_gexf)
    except Exception as e:
        print(f"Erro ao carregar {arquivo_gexf}: {e}")
        return

    if G.number_of_nodes() == 0:
        print(f"Sem nós para o período {periodo}.")
        return

    graus = dict(G.degree())
    top5_nos = sorted(graus, key=graus.get, reverse=True)[:5]

    tamanhos = [graus[n] * 10 for n in G.nodes()]  # nó menor
    pos = nx.spring_layout(G, seed=42, k=0.15)

    # Arestas
    cores_arestas = []
    larguras_arestas = []
    for u, v, dados in G.edges(data=True):
        u_perm = G.nodes[u].get("is_permanent", False)
        v_perm = G.nodes[v].get("is_permanent", False)
        cor = "red" if u_perm and v_perm else "black"
        cores_arestas.append(cor)

        citacoes = dados.get("citation_num", 1)
        larguras_arestas.append(float(citacoes) / 2.5)

    # Plotagem
    plt.figure(figsize=(12, 9))

    # Arestas
    nx.draw_networkx_edges(G, pos, edge_color=cores_arestas, width=larguras_arestas, alpha=0.7)

    # Nós com borda
    nx.draw_networkx_nodes(G, pos, node_color="skyblue", edgecolors='black',
                           linewidths=0.8, node_size=tamanhos)

    # Top 5 nós
    nx.draw_networkx_labels(G, pos,
                            labels={n: str(n) for n in top5_nos},
                            font_color="yellow", font_size=9, font_weight='bold')

    plt.title(f"Rede do Período {periodo}", fontsize=12)
    plt.axis("off")
    plt.tight_layout()
    
    # Salvar imagem
    plt.savefig(f"rede_{periodo}.png", format="png")
    plt.show()


def main():
    for periodo in periodos:
        arquivo = os.path.join(caminho_arquivos, f"{periodo}.gexf")
        if os.path.exists(arquivo):
            print(f"Visualizando período: {periodo}")
            visualizar_rede_por_periodo(arquivo, periodo)
        else:
            print(f"Arquivo não encontrado para o período: {periodo}")

if __name__ == "__main__":
    main()
