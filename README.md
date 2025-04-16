# Análise de Redes do PPgEEC (2010-2025)

Este repositório contém o código e os resultados da análise de redes de colaboração do Programa de Pós-Graduação em Engenharia Elétrica e de Computação (PPgEEC) durante o período de 2010 a 2025. A análise foi implementada em Python, utilizando bibliotecas especializadas para análise e visualização de redes.

## Visão Geral

O projeto analisa as redes de colaboração acadêmica do PPgEEC, examinando a evolução das métricas de rede ao longo do tempo e explorando padrões de colaboração entre pesquisadores. A análise foi dividida em três requisitos principais:

1. Análise temporal de métricas da rede
2. Visualização das redes em períodos específicos de avaliação
3. Análise de sub-grafos e redes ego

## Ferramentas e Bibliotecas Utilizadas

- **Python 3.8+**
- **NetworkX**: Para criação, manipulação e análise de estruturas de rede
- **Pandas**: Para manipulação e análise de dados
- **Matplotlib** e **Seaborn**: Para visualização de dados e gráficos
- **NumPy**: Para operações numéricas

##Estrutura do Projeto
Trabalho-U1-Redes-Temporais-de-Co-Autoria/
├── avaliacao_total/
│   └── ppgeec_2010_2025.gexf  # Base geral dos dados de 2010 a 2025
├── basedados/
│   ├── avaliacao_geral/
│   │   ├── ppgeec_2010_2012.gexf
│   │   ├── ppgeec_2013_2016.gexf
│   │   ├── ppgeec_2017_2020.gexf
│   │   └── ppgeec_2021_2024.gexf
│   └── anos/
│       ├── ppgeec_2010.gexf
│       ├── ppgeec_2011.gexf
│       ├── ppgeec_2012.gexf
│       └── ...  # Demais arquivos até 2025
├── Gráficos_requisitos/
│   ├── Requisito1/
│   │   ├── densidade_rede.png
│   │   ├── num_vertices.png
│   │   ├── num_arestas.png
│   │   ├── media_vizinhos.png
│   │   └── distribuicao_vizinhos.png
│   ├── Requisito2/
│   │   ├── rede_2010_2012.png
│   │   ├── rede_2013_2016.png
│   │   ├── rede_2017_2020.png
│   │   └── rede_2021_2024.png
│   └── Requisito3/
│       ├── subgrafo_comparacao.png
│       └── rede_ego.png
└── README.md

## Requisito 1: Análise Temporal (2010-2025)

### Metodologia

Para analisar o comportamento temporal da rede do PPgEEC, implementei as seguintes etapas:

1. Carreguei os dados da rede para cada ano do período 2010-2025
2. Calculei as métricas solicitadas para cada ano:
   - Densidade da rede
   - Número de vértices
   - Número de arestas
   - Número médio de vizinhos
   - Distribuição do número de vizinhos
3. Gerei visualizações para cada métrica ao longo do tempo
4. Destaquei os marcos importantes de avaliação do PPgEEC (2012, 2016, 2020, 2024)
5. Implementação
   -Abrir arquivo R1 que é referente ao código utilizado para geras gráficos e analises pro requisito 1.



### Principais Achados

Através da análise temporal, observei os seguintes padrões:

1. **Densidade da rede**: Houve um crescimento gradual até 2016, seguido de uma estabilização e posterior aumento a partir de 2020, indicando maior interconexão entre os pesquisadores do programa.

2. **Número de vértices**: Crescimento constante ao longo dos anos, com aceleração notável após 2016, sugerindo expansão do programa e aumento no número de pesquisadores.

3. **Número de arestas**: Crescimento mais acentuado que o número de vértices, especialmente após 2020, indicando maior colaboração entre os membros do programa.

4. **Número médio de vizinhos**: Tendência de crescimento, com destaque para os períodos após as avaliações do programa (2012, 2016, 2020), possivelmente refletindo esforços para aumentar colaborações.

5. **Distribuição de vizinhos**: Observou-se padrão de lei de potência típico de redes de colaboração científica, com poucos pesquisadores muito conectados e muitos com poucas conexões.

### Dificuldades e Hipóteses

**Dificuldades enfrentadas**:
- Tratamento de dados inconsistentes em alguns anos
- Escolha da escala adequada para visualizar métricas com diferentes ordens de grandeza
- Definição do melhor parâmetro para coloração dos histogramas

**Hipóteses**:
- O aumento na densidade e no número médio de vizinhos após os períodos de avaliação sugere que há um incentivo à colaboração após cada ciclo avaliativo
- Os picos de crescimento em 2016 e 2020 podem estar relacionados a políticas institucionais específicas ou a mudanças nos critérios de avaliação da CAPES
- A presença de "hubs" na rede (pesquisadores com muitas conexões) indica uma estrutura hierárquica nas colaborações do programa

## Requisito 2: Visualização das Redes por Período de Avaliação

### Metodologia

Para visualizar as redes nos períodos de avaliação do PPgEEC, implementei:

1. Agregação dos dados de rede em quatro períodos:
   - 2010-2012
   - 2013-2016
   - 2017-2020
   - 2021-2024

2. Aplicação dos parâmetros de visualização:
   - Tamanho do vértice proporcional ao número de vizinhos
   - Destaque para os 5 vértices com mais vizinhos
   - Cor das arestas: vermelha para conexões entre membros permanentes, preta para as demais
   - Largura da aresta proporcional ao número de citações

3. Implementação
   -Abrir arquivo R1 que é referente ao código utilizado para geras gráficos e analises pro requisito 1.

### Principais Achados

Após analisar as visualizações para cada período, identifiquei:

1. **Período 2010-2012**: Rede ainda esparsa com poucos membros permanentes colaborando entre si. Os top 5 vértices apresentam conexões limitadas, sugerindo um programa em fase inicial de desenvolvimento.

2. **Período 2013-2016**: Aumento significativo na complexidade da rede, com formação de comunidades visíveis. Surgimento de arestas mais espessas, indicando aumento no número de citações por colaboração.

3. **Período 2017-2020**: Intensificação das colaborações entre membros permanentes (mais arestas vermelhas), sugerindo maior coesão institucional. Os top 5 vértices começam a apresentar características de hubs na rede.

4. **Período 2021-2024**: Rede densamente conectada com múltiplas comunidades. Arestas significativamente mais espessas entre os principais pesquisadores, indicando colaborações com alto impacto (muitas citações).

### Dificuldades e Hipóteses

**Dificuldades enfrentadas**:
- Visualização de redes muito densas nos períodos mais recentes
- Escolha de layout adequado para representar a estrutura da rede sem sobreposições
- Calibração dos parâmetros visuais (tamanho dos nós, espessura das arestas) para manter legibilidade

**Hipóteses**:
- A evolução da rede sugere um programa que evoluiu de grupos isolados para uma estrutura mais integrada
- A concentração de colaborações em torno de poucos pesquisadores (top 5) pode indicar lideranças científicas consolidadas
- O aumento de arestas vermelhas ao longo do tempo sugere uma política bem-sucedida de integração entre membros permanentes

## Requisito 3: Análise de Sub-grafo e Rede Ego

### Metodologia

Para gerar e analisar o sub-grafo e a rede ego, implementei:

1. Desenvolvimento de uma metodologia para definir o limiar X (número mínimo de vizinhos):
   - Calculei a média e o desvio padrão do número de vizinhos na rede geral
   - Defini X como a média mais um desvio padrão, identificando os vértices acima da média

2. Geração do sub-grafo contendo apenas os vértices com X ou mais vizinhos

3. Comparação da densidade entre o grafo geral e o sub-grafo

4. Seleção de um vértice representativo e análise da sua rede ego (rede formada pelo vértice e seus vizinhos diretos)

5. Implementação
   -Abrir arquivo R3 que é referente ao código utilizado para geras gráficos e analises pro requisito 3.

### Principais Achados

Os resultados dessa análise revelaram:

1. **Definição do limiar X**: Após calcular a média e o desvio padrão, determinei X = 12 vizinhos como ponto de corte para identificar pesquisadores altamente conectados.

2. **Comparação de densidades**:
   - Densidade da rede geral: 0.021
   - Densidade do sub-grafo: 0.156
   
   A diferença significativa (aproximadamente 7 vezes maior) indica que os pesquisadores mais conectados formam um núcleo coeso dentro da rede maior.

3. **Análise da rede ego**: Selecionei o pesquisador com maior número de conexões para análise da rede ego. Observei:
   - Alto coeficiente de clustering (0.412), indicando que muitos dos vizinhos deste pesquisador também colaboram entre si
   - Presença de "pontes" na rede ego, conectando grupos distintos de pesquisadores
   - Distribuição heterogênea de intensidade de colaboração (citações)

### Dificuldades e Hipóteses

**Dificuldades enfrentadas**:
- Definição de um critério adequado para o limiar X que fosse significativo para o contexto do programa
- Visualização clara da rede ego devido ao grande número de conexões
- Interpretação da densidade comparativa considerando as diferenças estruturais entre os grafos

**Hipóteses**:
- O sub-grafo identificado pode representar o "núcleo científico" do programa, responsável pela maior parte da produção
- A alta densidade do sub-grafo sugere um grupo coeso de pesquisadores, possivelmente com áreas de pesquisa sobrepostas
- A estrutura da rede ego analisada indica um pesquisador que atua como "ponte" entre diferentes grupos de pesquisa

## Conclusões Gerais

A análise da rede de colaboração do PPgEEC ao longo de 15 anos (2010-2025) revelou:

1. **Evolução consistente**: O programa demonstrou crescimento constante em número de pesquisadores e colaborações, com aceleração nos períodos recentes.

2. **Impacto das avaliações**: Os períodos após cada avaliação (2012, 2016, 2020) foram marcados por mudanças estruturais na rede, sugerindo resposta às políticas de incentivo à colaboração.

3. **Formação de comunidades**: A rede evoluiu de grupos isolados para uma estrutura mais integrada, com aumento significativo na colaboração entre membros permanentes.

4. **Núcleo coeso**: Identificamos um sub-grafo de pesquisadores altamente conectados que forma um núcleo científico coeso dentro do programa.

5. **Pesquisadores-ponte**: A análise de redes ego revelou pesquisadores que atuam como conectores entre diferentes grupos, contribuindo para a coesão geral da rede.

## Próximos Passos

Possíveis extensões para este estudo incluem:

1. Análise de comunidades para identificar subáreas de pesquisa
2. Correlação entre métricas de rede e produtividade científica
3. Análise de redes dinâmicas para rastrear a evolução de colaborações específicas
4. Comparação com redes de outros programas de pós-graduação similares

## Instruções de Uso

1. Clone este repositório
2. Execute os notebooks na ordem numérica para reproduzir as análises
3. Instale as bibliotecas necessárias que é pedida de para cada código.

# Bibliotecas necessárias para instalar:
1. Networkx
2. Pandas
3. Joypy
4. Seaborn
5. Matplotlib

## Ferramentas auxiliares de ia utilizadas:
1. ChatGPT
2. Claude.ai