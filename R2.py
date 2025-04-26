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
        larguras_arestas.append(float(citacoes)/10)

    # Plotagem
    plt.figure(figsize=(12, 9))

    # Arestas
    nx.draw_networkx_edges(G, pos, edge_color=cores_arestas, width=larguras_arestas, alpha=0.7)
    
        # Nós comuns (não estão no top5)
    nos_comuns = [n for n in G.nodes() if n not in top5_nos]
    nx.draw_networkx_nodes(G, pos,
                        nodelist=nos_comuns,
                        node_color="#1C8394",
                        edgecolors='#1C8394',
                        linewidths=0.8,
                        node_size=[tamanhos[i] for i, n in enumerate(G.nodes()) if n in nos_comuns],
                        alpha=0.6)

    # Top 5 nós (com outra cor)
    nx.draw_networkx_nodes(G, pos,
                        nodelist=top5_nos,
                        node_color="#390D02",    # <<< Aqui define a cor dos top 5
                        edgecolors='#A52502',
                        linewidths=1.0,
                        node_size=[tamanhos[i] for i, n in enumerate(G.nodes()) if n in top5_nos],
                        alpha=1.0)

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
