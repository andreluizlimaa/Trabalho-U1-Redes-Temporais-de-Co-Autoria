# Análise Temporal de Redes de Coautoria Acadêmica

by </br>
[André Luiz Lima Souza](https://github.com/andreluizlimaa) </br>
[Daniel Bruno Trindade da Silva](https://github.com/daniel-trindade)

***

## Visão Geral

Neste projeto, foi realizada uma análise das redes de colaboração científica do Programa de Pós-Graduação em Engenharia Elétrica e de Computação (PPgEEC), abrangendo o período de 2010 a 2025. O estudo examinou a evolução das métricas da rede ao longo do tempo e buscou identificar padrões de colaboração entre pesquisadores acadêmicos.

O principal objetivo foi reforçar os conceitos relacionados a grafos por meio da aplicação prática da biblioteca NetworkX, da linguagem Python. Esta atividade foi desenvolvida no contexto da disciplina de **Algoritmos e Estruturas de Dados II**.

***

## Ferramentas e Bibliotecas Utilizadas

- **Python 3.8+**
- **NetworkX**: Para criação, manipulação e análise de estruturas de rede
- **Pandas**: Para manipulação e análise de dados
- **Matplotlib** e **Seaborn**: Para visualização de dados e gráficos
- **NumPy**: Para operações numéricas

As versões de cada uma delas pode ser encontrada no arquivo requirements.txt.

***

## Análise dos dados

A análise foi dividida em três requisitos principais:

1. Análise temporal de métricas da rede
2. Visualização das redes em períodos específicos de avaliação
3. Análise de sub-grafos e redes ego

vamos explicitar a metodologia de cada um deles isoladamente.

### Requisito 1: Análise Temporal (2010-2025)

#### Metodologia

Para analisar o comportamento temporal da rede do PPgEEC, foi implementado o código R1.py que seguiu as seguintes etapas:

1. Foram carregados os dados da rede para cada ano do período 2010-2025
2. Calculado as métricas solicitadas para cada ano:
   - Densidade da rede - Que mostra o quão colaborativo são os acadêmicos entre si.
   - Número de vértices - Representa o Número de acadêmicos envolvidos;
   - Número de arestas - Número de colaborações entre acadêmicos;
   - Número médio de vizinhos ou Gráu Médio - Quantidade média de colaborações por acadêmico;
   - Distribuição do número de vizinhos - Mostra o quão a rede está dispersa ou se existem hubs (rede centralizada)
3. Foi gerada as visualizações gráficas para cada métrica ao longo do tempo
   - Um gráfico de linhas com os cada uma das métricas expostas no item 2;
   - Um gráfico Ridgeline que mostra a destribuição do número de conexões por pesquisador a cada ano;
4. Foram destacados os marcos importantes de avaliação do PPgEEC (2012, 2016, 2020, 2024)

##### Gráficos:
![Métricas dos grafos ao Longo dos anos](graficos/Requisito1/Métricas%20dos%20grafos%20ao%20Longo%20dos%20anos.png)
![Gráfico da Função de densidade de probabilidade](graficos/Requisito1/Gráfico%20da%20Função%20de%20densidade%20de%20probabilidade.png)

#### Análise

Através da análise temporal, foi possível observar o seguinte:

1. **Densidade da rede**: A densidade se mantém bastante baixa durante todo o período tendo como valor médio 0.0299 ao longo dos anos. Esse comportamento é esperado em redes de colaboração científica (onde não é comum todos os acadêmicos estarem conectados entre si). Não há grandes variações nesse padão, o que sugere que, mesmo com o aumento no número de nós e arestas, ou seja, acadêmicos e produções, a proporção de conexões possíveis que de fato ocorrem segue estável.

2. **Número de Nós (Acadêmicos)**: Crescimento consistente até 2019, indicando aumento de participantes na rede. Pequena estabilização entre 2020 e 2024, sugerindo maturidade no número de participantes. Queda significativa em 2025, o que pode ser explicado por dados incompletos.  

3. **Número de arestas (Produções em conjunto)**: Tendência de crescimento, com destaque para os períodos após as avaliações do programa (2012, 2016, 2020), possivelmente refletindo esforços para aumentar colaborações.

4. **Número médio de vizinhos**: Crescimento constante com uma média de 8 conexões para cada acadêmico em 2010, chegando a quase 14 conexões em média por acadêmico em 2022.

Já no gráfico Ridgeline observamos que
 1. As curvas possuem um leve deslocamento para a direita, isso demonstra que ao longo dos anos os pesquisadores passaram a ter mais colaborações;
 2. A forma das distribuições mostra que, na maioria dos anos, a maior parte dos pesquisadores tem grau pequeno, com poucos tendo graus muito altos (comportamento típico de redes reais, como as de colaboração científica).

 #### Dificuldades enfrentadas:

- Tratamento de dados inconsistentes em alguns anos
- Escolha da escala adequada para visualizar métricas com diferentes ordens de grandeza
- Definição do melhor parâmetro para coloração dos histogramas


#### Conclusão

- O aumento na densidade e no número médio de vizinhos após os períodos de avaliação sugere que há um incentivo à colaboração após cada ciclo avaliativo;
- Houve um crescimento na rede de colaboração do PPgEEC entre 2010 e 2019, com aumento no número de participantes (nós) e colaborações (arestas).
- O grau médio e a densidade mantiveram-se estáveis ou cresceram levemente, o que indica uma melhoria na integração dos pesquisadores.
- Os picos de grau médio e número de arestas podem estar associados a eventos institucionais, como reestruturações ou incentivos à pesquisa colaborativa.
- A distribuição dos graus mostra que a maioria dos pesquisadores tem poucas conexões, enquanto poucos atuam como hubs (nós muito conectados), padrão típico em redes científicas.
### Requisito 2: Visualização das Redes por Período de Avaliação

#### Metodologia

Para visualizar as redes nos períodos de avaliação do PPgEEC, implementamos:

1. Agregação dos dados de rede em quatro períodos (Períodos de avaliação do programa):
   - 2010-2012
   - 2013-2016
   - 2017-2020
   - 2021-2024

2. Aplicação dos parâmetros de visualização:
   - Raio dos vértices proporcional ao número de vizinhos
   - Destaque para os 5 vértices com mais vizinhos
   - Cor das arestas: vermelha para conexões entre membros permanentes, preta para as demais
   - Largura da aresta proporcional ao número de citações

3. Implementação
   - O código utilizado para gerar os grafos se enncontram no aqrquivo R2.py;

##### Gráfos:

- Período 2010-2012
![Período 2010-2012](graficos/Requisito2/rede_2010-2012.png)
- Período 2013-2016
![Período 2010-2012](graficos/Requisito2/rede_2013-2016.png)
- Período 2017-2020
![Período 2010-2012](graficos/Requisito2/rede_2017-2020.png)
- Período 2021-2024
![Período 2010-2012](graficos/Requisito2/rede_2021-2024.png)

#### Análise

Após analisar as visualizações para cada período, foi identificado:

1. **Período 2010-2012**: Rede ainda esparsa com poucos membros permanentes colaborando entre si. Os top 5 vértices apresentam conexões limitadas, sugerindo um programa em fase inicial de desenvolvimento.

2. **Período 2013-2016**: Aumento significativo na complexidade da rede, com formação de comunidades visíveis. Surgimento de arestas mais espessas, indicando aumento no número de citações por colaboração.

3. **Período 2017-2020**: Intensificação das colaborações entre membros permanentes (mais arestas vermelhas), sugerindo maior coesão institucional. Os top 5 vértices começam a apresentar características de hubs na rede.

4. **Período 2021-2024**: Rede densamente conectada com múltiplas comunidades. Arestas significativamente mais espessas entre os principais pesquisadores, indicando colaborações com alto impacto (muitas citações).

#### Dificuldades
- Visualização de redes muito densas nos períodos mais recentes
- Escolha de layout adequado para representar a estrutura da rede sem sobreposições
- Calibração dos parâmetros visuais (tamanho dos nós, espessura das arestas) para manter legibilidade

#### Conclusão:
- A evolução da rede sugere um programa que evoluiu de grupos isolados para uma estrutura mais integrada
- A concentração de colaborações em torno de poucos pesquisadores (top 5) pode indicar lideranças científicas consolidadas
- O aumento de arestas vermelhas ao longo do tempo sugere uma política bem-sucedida de integração entre membros permanentes

### Requisito 3: Análise de Sub-grafo e Rede Ego

#### Metodologia

Para uma melhor avaliarmos o potencial do trabalho com grafos foram solicitados 3 grafos, são eles:
1. Um grafo da rede geral
2. Um sub-grafo a partir da rede geral (2010 - 2025) contendo apenas vértices que possuem pelo menos _x_ vizinhos.
3. O Grafo de uma rede de ego de um vertice da rede;

Para gerar esses grafos foi utilizamos as bibliotecas NetworkX que é objeto de estudo, juntamente com a matplotlib

1. Gráfico geral:
![Grafo da Rede Geral](/graficos/Requisito3/grafo-geral.png)

2. Sub-Grafo
- Para definição do valor mínimo de vizinhos _x_, adotou-se a metodologia baseada no percentil 80 da distribuição de graus da rede geral. Assim, consideramos apenas os 20% nós mais conectados, focando a análise nos vértices centrais com maior potencial de influência e conectividade.

![Sub-grafo com os 20% mais conectados](/graficos/Requisito3/Sub-Grafo%20%2080png)

3. Para a rede-ego foi escolhido um no que possuisse uma forte conexão com seus vizinhos e que houvesse um número equilibrado de conexões para facilitar a visualização. Nesse frafo também diferimos os tamanhos dos nós para que eles demonstrassem o grau que possuem.

![Rede-Ego](/graficos/Requisito3/rede_ego_Kleyton.png)
### Principais Achados

1. **Grafo Geral** 
- Foi possível observar que o meio da rede está super denso, cheio de conexões entre os nós. Isso sugere a presença de vários hubs (nós muito conectados) ou comunidades sobrepostas. Pode também representar um núcleo principal de interações ou colaborações intensas;
- Foi possível perceber também a existencia de nós periféricos com poucos vizinhos, o que indica a existencia de participantes com pouca interação;
- A diferença entre o núcleo denso e a periferia sugere que talvez sua rede siga uma distribuição de graus do tipo "power-law", ou seja, poucos nós com muitas conexões e muitos nós com poucas, isso é algo muito comum em redes sociais, científicas, etc.

2. **Subgrafo**
- Tomamos os 20% nós mais conectados da rede geral para formar o subgrafo, com isso podemos podemos ver como os principais vertices, ou seja, os principais acadêmicos dessa rede se interconectão e como é a interação entre eles.

3. **Rede-Ego** 
- O nó central está muito bem conectado, visualmente, ele se conecta com quase todos os nós ao seu redor. Os nós ao redor também estão muito interconectados entre si, formando uma rede bastante densa. Isso indica que não é só o central que conecta os vizinhos também têm fortes conexões diretas entre si. Em termos de rede, isso reflete alta coesão (pessoas que são próximas entre si, formando um cluster compacto).


***

#  falta revisar
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





# Bibliotecas necessárias para instalar:
1. Networkx
2. Pandas
3. Joypy
4. Seaborn
5. Matplotlib

## Ferramentas auxiliares de ia utilizadas:
1. ChatGPT
2. Claude.ai