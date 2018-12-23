
# coding: utf-8

# In[1]:


from IPython.display import HTML
HTML('''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
Essa análise foi realizada usando a linguagem de programação Python. O código foi retirado para facilitar a leitura.
Para exibir/ocultar o código clique <a href="javascript:code_toggle()">aqui</a>.''')


# <h1>Índice<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Introdução" data-toc-modified-id="Introdução-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Introdução</a></span></li><li><span><a href="#Carga,-limpeza-e-transformação-dos-dados" data-toc-modified-id="Carga,-limpeza-e-transformação-dos-dados-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Carga, limpeza e transformação dos dados</a></span><ul class="toc-item"><li><span><a href="#Tratamentos-necessários:" data-toc-modified-id="Tratamentos-necessários:-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Tratamentos necessários:</a></span></li><li><span><a href="#Transformação-e-formatação-dos-dados" data-toc-modified-id="Transformação-e-formatação-dos-dados-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Transformação e formatação dos dados</a></span></li><li><span><a href="#Convertendo-os-valores-da-coluna-vlr_despesa" data-toc-modified-id="Convertendo-os-valores-da-coluna-vlr_despesa-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Convertendo os valores da coluna vlr_despesa</a></span></li></ul></li><li><span><a href="#Análise-Exploratória" data-toc-modified-id="Análise-Exploratória-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Análise Exploratória</a></span><ul class="toc-item"><li><span><a href="#Como-se-comportam-os-gastos-com-cotas-parlamentares-ao-longo-do-tempo?-Existe-alguma-tendência-de-aumento-ou-redução-desse-custo?-Existe-sazonalidade?" data-toc-modified-id="Como-se-comportam-os-gastos-com-cotas-parlamentares-ao-longo-do-tempo?-Existe-alguma-tendência-de-aumento-ou-redução-desse-custo?-Existe-sazonalidade?-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>Como se comportam os gastos com cotas parlamentares ao longo do tempo? Existe alguma tendência de aumento ou redução desse custo? Existe sazonalidade?</a></span></li><li><span><a href="#Quais-foram-os-parlamentares-que-mais-consumiram-recursos-?-E-quais-foram-os-que-menos-consumiram-recursos?" data-toc-modified-id="Quais-foram-os-parlamentares-que-mais-consumiram-recursos-?-E-quais-foram-os-que-menos-consumiram-recursos?-3.2"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>Quais foram os parlamentares que mais consumiram recursos ? E quais foram os que menos consumiram recursos?</a></span></li><li><span><a href="#Políticos-que-usaram-menos-valor-das-cotas-paralamentares:" data-toc-modified-id="Políticos-que-usaram-menos-valor-das-cotas-paralamentares:-3.3"><span class="toc-item-num">3.3&nbsp;&nbsp;</span>Políticos que usaram menos valor das cotas paralamentares:</a></span></li><li><span><a href="#Quais-são-as-categorias-de-despesas-mais-onerosas-dentre-os-recursos-destinados-às-cotas-parlamentares?" data-toc-modified-id="Quais-são-as-categorias-de-despesas-mais-onerosas-dentre-os-recursos-destinados-às-cotas-parlamentares?-3.4"><span class="toc-item-num">3.4&nbsp;&nbsp;</span>Quais são as categorias de despesas mais onerosas dentre os recursos destinados às cotas parlamentares?</a></span></li><li><span><a href="#Qual-é-o-gasto-por-estado?" data-toc-modified-id="Qual-é-o-gasto-por-estado?-3.5"><span class="toc-item-num">3.5&nbsp;&nbsp;</span>Qual é o gasto por estado?</a></span></li><li><span><a href="#Qual-estado-tem-maior-número-de-representantes-?" data-toc-modified-id="Qual-estado-tem-maior-número-de-representantes-?-3.6"><span class="toc-item-num">3.6&nbsp;&nbsp;</span>Qual estado tem maior número de representantes ?</a></span></li><li><span><a href="#Quais-partidos-mais-consomem-a-cota-parlamentar-?" data-toc-modified-id="Quais-partidos-mais-consomem-a-cota-parlamentar-?-3.7"><span class="toc-item-num">3.7&nbsp;&nbsp;</span>Quais partidos mais consomem a cota parlamentar ?</a></span></li><li><span><a href="#Quais-parlamentares-tem-a-maior-média-de-gastos?" data-toc-modified-id="Quais-parlamentares-tem-a-maior-média-de-gastos?-3.8"><span class="toc-item-num">3.8&nbsp;&nbsp;</span>Quais parlamentares tem a maior média de gastos?</a></span></li><li><span><a href="#Gastos-com-alimentação" data-toc-modified-id="Gastos-com-alimentação-3.9"><span class="toc-item-num">3.9&nbsp;&nbsp;</span>Gastos com alimentação</a></span></li><li><span><a href="#Fretamento-de-aeronvaves" data-toc-modified-id="Fretamento-de-aeronvaves-3.10"><span class="toc-item-num">3.10&nbsp;&nbsp;</span>Fretamento de aeronvaves</a></span></li></ul></li><li><span><a href="#Conclusão" data-toc-modified-id="Conclusão-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Conclusão</a></span></li></ul></div>

# # Analise dos gastos com cotas parlamentares
# 
# 
# ### Proposta de análise:
# 
# Aqui me proponho a realizar uma análise exploratória sobre as **despesas com cotas parlamentares do congresso nacional no período de 2009 à 2017**. 
# 
# As cotas parlamentares são um valor de reembolso ao qual os políticos (senadores e deputados) tem direito, para gastos relacionados exclusivamente ao exercício de sua função. O reembolso pode ser solicitado para gastos com alimentação, locomoção, contratação de serviços entre outros. Os dados utilizados foram extraídos do [portal de dados abertos](http://www2.camara.leg.br/transparencia/cota-para-exercicio-da-atividade-parlamentar/dados-abertos-cota-parlamentar) da câmara federal. A a descrição dos dados está disponível [Aqui](http://www2.camara.leg.br/transparencia/cota-para-exercicio-da-atividade-parlamentar/explicacoes-sobre-o-formato-dos-arquivos-xml).
# 
# O análise será realizada passando pelas seguintes etapas:
# 
#    
# ### 1. Carga, limpeza e transformação dos dados:
# 
# Nessa etapa irei explorar o conjunto de dados em busca de anomalias que precisam ser tratadas para viabilizar a devida análise. Isso envolve detectar valores ausentes, corrigir o formato de dados armazenados de forma incorreta e criar e/ou transformar os dados a partir dos atributos existentes. 
# 
# ### 2. Análise exploratória
# 
# Após finalizar o tratamento e preparação dos dados, iniciarei a análise exploratória dos dados. 
# 
# 
# ### 3. Conclusão
# 
# Nessa seção demonstrarei as conclusões da análise e compartilharei os ***insghts*** descobertos, bem como novas possíveis linhas de análise.
# 
# 
# Então, mãos à obra! 
# 
#                              .................................................................

# # Introdução

# # Carga, limpeza e transformação dos dados

# Importanto as bibliotecas necessárias para a análise e carregando os dados.

# In[2]:


import pandas as pd # para manipulação e limpeza dos dados
import numpy as np  # operações matemáticas e com vetores

from datetime import datetime # módulo para uso de ferramentas de data e hora

get_ipython().run_line_magic('matplotlib', 'inline')


import matplotlib.pyplot as plt # gráficos
import seaborn as sns           # gráficos e ferramentas de estatísticas
sns.set_style('whitegrid')

# configurações padrão para os gráficos


plt.rc('figure', figsize=(10,8))
plt.style.use('ggplot')

# Plotly umas das bibliotecas mais incríveis para dataviz ! Irei usá-la neste caso devido a escala dos valores do dataset (na casa de centenas
# de milhões, essa biblioteca torna a leitura desses valores muito mais clara) 

from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
init_notebook_mode(connected=True)

import warnings
warnings.filterwarnings("ignore")



# In[3]:


# Criando as funções para plotagem

############################# Barras ######################################################

def plot_bar(dados, graf_title=None, xaxis_title=None, yaxis_title=None, color=None):
    
    '''Plota gráfico de barras da Plotly
    
    Dados: Dados agrupados em duas colunas
    
    graf_tile:  string Título do gráfico
    
    xaxis_title: string Título eixo x
    
    yaxis_title: string Título do eixo y
    
    '''
    
    dados_a = dict(dados)
    y_vals = dados.values
    x_vals = dados_a.keys()
    x_vals = list(x_vals)
    
    dados_b = [go.Bar(x= x_vals,
                   y = y_vals,
                marker = dict(color=color),
                  orientation= 'v')]
    
    
    layout = go.Layout(title= graf_title, 
                   yaxis=dict(autorange=True, title= yaxis_title,
                              tickfont=dict(size=12)
                             ), xaxis=dict(title= xaxis_title, tickfont=dict(size=8)))



    fig = go.Figure(data=dados_b, layout=layout)
    iplot(fig, filename='basic-bar')
    
############################# Pizza ######################################################

def graf_pie(dados, graf_title=None):
    
    '''Plota gráfico de pizza da Plotly
    
    Dados: Dados agrupados em duas colunas
    
    graf_tile:  string Título do gráfico
    
        
    '''
    dados = dict(viagens_edio)
    labels = list(dados.keys())
    values = list(dados.values())

    pie = go.Pie(labels=labels, values=values, title=graf_title)

    iplot([pie], filename='pie basico')


# O conjunto de dados tem um número considerável de colunas. As colunas que acredito que podem auxiliar a responder as questões propostas são:
# 
# *  txNomeParlamentar - Nome do parlamentar;
# *  nuLegislatura - Ano início da legislatura do parlamentar;
# *  sgUF - Sigla do estado que o parlamentar representa;
# *  sgPartido - Sigla do partido;
# *  txtDescricao - Descrição do tipo de despesa;
# *  txtDescricaoEspecificacao - descrição detalhada da despesa;
# *  txtFornecedor - nome do fornecedor do serviço;
# *  vlrLiquido - O valor que será reembolsado para o parlamentar;
# *  numMes - Mês do reembolso;
# *  numAno - Ano do reembolso;
# 
# Essas colunas irão compor o conjunto de dados.

# Carga dos dados: Os dados estão divididos em 9 arquivos, um para cada ano. Não faz sentido carregar um por um, por isso, crio um loop `for` para carregar todos os datasets e em seguida uso a função `concat()` do pandas para unir todos os arquivos em um único dataframe.

# In[4]:


anos = range(2009,2018) # Até 2018, pois range exclui o último valor

# Lista com as colunas que serão mantidas para análise
colunas = ['txNomeParlamentar', 'nuLegislatura', 'sgUF', 'sgPartido','txtDescricao', 'txtDescricaoEspecificacao',
          'txtFornecedor', 'vlrLiquido', 'numMes', 'numAno']

dfs = []

for ano in anos:
    df = pd.read_csv('Ano-{}.csv'.format(ano), sep=';', error_bad_lines=True, usecols=colunas,  index_col=False, dtype='unicode')
    dfs.append(df)
    df_completo = pd.concat(dfs, ignore_index=True)
    

# Renomeando as colunas em letra minúscula para facilitar a manipulação e deixar mais intuitivo

cols = ['nome_parlamentar', 'legislatura', 'uf', 'partido', 'desc_despesa', 'desc_especifica',
 'nome_fornecedor', 'vlr_despesa', 'mes_despesa', 'ano_despesa']

df_completo.columns = cols
    


# In[5]:


df_completo.head() # Confirmando se tudo correu bem


# In[6]:


df_completo.tail() # as últimas 5 linhas do dataset.


# In[7]:


df_completo.isnull().sum() # Avaliando valores nulos e tipos de dados


# In[8]:


df_completo.info() # Verificando os tipos de dados do dataset


# Agora que os dados foram carregados, iniciaremos o processo de tratamento dos dados. Como vimos todos os dados estão com o formato de `object`. Isso aconteceu pois especifiquei que o dataset teria apenas um tipo passando o parâmetro `dtype` com o argumento 'unicode' no momento de importá-lo. Isso foi necessário devido ao tamanho do dataset (mais de 3MM de linhas), o pandas reconhece o tipo de dados de cada coluna apenas após percorre-la por completo. Essa tarefa neste dataset exije muita performance de memória e está sujeito a erros, por isso, especifiquei um único formato para todo o dataset, livrando o pandas dessa tarefa.
# 
# 

# ## Tratamentos necessários:
# 
# 
# 
# **legislatura**, **uf**, **partido** e **desc_especifica** apresentam valores ausentes. A última apresenta um número considerável. Iremos analisar a melhor estratégia para tratar este problema.
# 
# **Formatação dos dados**:
# 
# Todos os dados estão no formato `object` o que é um problema. Nem todas as colunas devem armazenar dados neste formato. A coluna **vlr_despesa** precisa ser convertida para dado numérico, no caso, `float` pois refere-se a valores contábeis.
# 
# **mes** e **ano** serão convertidas para `int`, assim é possível ordená-las.

# **desc_especifica**

# In[9]:


df_completo.desc_especifica.value_counts()


# Vamos entender o motivo de existirem tantos valores ausentes.

# In[10]:


null_desc_especifica = df_completo[df_completo['desc_especifica'].isnull() == True] # filtrando os dados ausentes


# In[11]:


null_desc_especifica.shape


# Analisando as primeiras linhas para entender a relação com as demais colunas...

# In[12]:


null_desc_especifica.head()


# Quais são os gastos quando não há valores na **desc_especifica** ?

# In[13]:


null_desc_especifica.desc_despesa.value_counts()


# Ao que parece o único gasto ausente entre as categorias, é com combustível...
# 
# Vamos observar somente as linhas que estejam preenchidas.

# In[14]:


dados_preenchidos = df_completo[df_completo['desc_especifica'].isnull() == False]
dados_preenchidos.head()


# In[15]:


dados_preenchidos.desc_despesa.value_counts() # Estes são os valores preenchidos


# In[16]:


df_completo.desc_especifica.value_counts()


# **Conclusão:** 
# A coluna **desc_especifica** só é preenchida quando o parlamentar faz uso de sua verba para aquisição de combustíveis. O número de vezes que a descrição 'COMBUSTÍVEIS E LUBRIFICANTES.' aparece na coluna **desc_despesa** é o mesmo número de células preenchidas na **desc_especifica**.
# 
# O dado 'Sem especificações' é um valor válido, pois refere-se ao uso de serviços de lubrificantes e combustíveis, mas sem a especificação do veículo utilizado. Irei preencher os valores ausentes com a mesma informação.

# In[17]:


df_completo.desc_especifica.fillna('Sem especificações', inplace=True)


# In[18]:


print('Quantidade de valores nulos na coluna desc_especifica: {}'.format(df_completo.desc_especifica.isnull().sum()))

df_completo.desc_especifica.value_counts()      


# Observando estes dados, um novo questionamento me vem em mente. **Quais são os parlamentares que gastaram a cota com combustível de aeronave?**
# 
# Eles já não gastam com passagem aérea? 

# In[19]:


df_completo.isnull().sum()


# Precisamos tratar as colunas **uf**,**partido** e **legislatura**. Pensando que o foco da análise está voltada para entender os gastos, não vejo problema em preencher estes dados com a informação "Sem informação". Assim não perdemos dados relativos aos gastos, o dado mais importante para essa análise. 

# In[20]:


df_completo.uf.fillna('Sem informação', inplace=True)

df_completo.legislatura.fillna('Sem informação', inplace=True)

df_completo.partido.fillna('Sem informação', inplace=True)


# In[21]:


# Confirmando se ainda existem valores nulos
df_completo.isnull().sum()


# Não temos mais valors nulos em nosso conjunto de dados.

# ## Transformação e formatação dos dados
# Agora podemos seguir para a fase de transformação dos dados. 

# ## Convertendo os valores da coluna vlr_despesa

# In[22]:


valor = df_completo.vlr_despesa
valor = [float(x.replace(',','.')) for x in valor ] # Usando um loop para converter um valor por vez...
valor = pd.Series(valor)
df_completo['vlr_despesa'] = valor
df_completo.info()


# Dado convertido com sucesso ! 

# Vamos converter as colunas 'ano' e 'mes' para `int`.

# In[23]:


df_completo['mes_despesa'] = df_completo['mes_despesa'].astype(int)
df_completo['ano_despesa'] = df_completo['ano_despesa'].astype(int)


# In[24]:


df_completo.info()


# # Análise Exploratória
# 
# Agora que os dados estão limpos e preparados, podemos iniciar a nossa exploração. Iremos começar com perguntas bem básicas, a fim de conhecer melhor o conjunto de dados.
# 
# a. Como se comportam os gastos com cotas parlamentares ao longo do tempo? Existe alguma tendência de aumento ou redução desse custo? Existe sazonalidade?
# 
# b. Quais foram os parlamentares que mais consumiram recursos? 
# 
# c. Quais foram os que menos consumiram recursos?
# 
# d. Quais são as categorias de despesas mais onerosas dentre os recursos destinados às cotas
# parlamentares?
# 
# e. Qual é o gasto por estado?
# 
# f. Quais estados tem maior número de representantes?
# 
# g. Quais partidos mais consomem a cota parlamentar?
# 
# h. Qual a média de gastos por parlamentar?
# 
# 
# 
# 
# 
# Primeiro vamos ver um rápido resumo do conjunto de dados:

# In[26]:


df_completo.describe(include='all').round()


# Com base neste quadro de resumo, já conseguimos ver algumas informações interessantes rapidamente. Por exemplo:
# 
# * A média de reembolso, considerando o período de 2009 à 2017, é de 535 reais;
# 
# * O maior reembolso/pagamento foi de 215 mil reais;
# 
# * O pedido mais comum é o reembolso de bilhetes / passagens aéreas;
# 
# * O fornecedor que mais aparece no dataset é a Gol - Linhas aéreas;
# 
# * Vanderlei Macris é o político mais solicitou reembolsos.
# 
# Esse é um breve resumo de algumas características do dataset.
# 
# Agora vamos buscar responder as perguntas propostas:

# ## Como se comportam os gastos com cotas parlamentares ao longo do tempo? Existe alguma tendência de aumento ou redução desse custo? Existe sazonalidade?
# 
# Vamos entender como os gastos com cotas parlamentares evoluíram ao longo do tempo. Para isso, vamos plotar um gráfico simples de linha para observar a evolução dos gastos ao longo dos anos.

# In[27]:


gastos_anuais = df_completo.groupby('ano_despesa')['vlr_despesa'].sum()

anuais = dict(gastos_anuais)
x = gastos_anuais.values
y = anuais.keys()
y = list(y)

data = [go.Line(x= list(y),
                 y=x,
               orientation= 'v')]

layout = go.Layout(title='Gastos por ano', 
                   yaxis=dict(autorange=True, title= 'Gastos',
                              tickfont=dict(size=12)
                             ), xaxis=dict(title='Ano', tickfont=dict(size=10)))



fig = go.Figure(data=data, layout=layout)
iplot(fig, filename='basic-bar')


# 
# * Em 2016 os gastos atingiram 221 milhões. O crescimento em relação à 2009 foi de 93%; 
# 
# * A crescente nos gastos ocorreu mesmo entre os anos de 2015 e 2016, período em que o Brasil esteve mergulhado em uma de suas maiores recesssões, tendo quedas consecutivas no PIB, sendo 3,8% e 3,6% em 2015 e 2016 respectivamente; 
# 
# * Mesmo a [pior crise desde 1945](http://g1.globo.com/jornal-hoje/noticia/2017/03/brasil-vive-pior-recessao-da-historia.html), não foi capaz de frear a subida dos gastos da classe política;
# 
# 

# Vamos verificar se existe sazonalidade nos gastos com cotas. Para isso, vamos plotar os últimos três anos dos gastos parlamentares em um único gráfico acredito que um período de 36 meses seja suficiente para encontrar um padrão ao longo do tempo.

# In[28]:


# Criando um conjunto de dados somente com os últimos 3 anos

ano_2015 = df_completo[df_completo['ano_despesa'] == 2015]
ano_2016 = df_completo[df_completo['ano_despesa'] == 2016]
ano_2017 = df_completo[df_completo['ano_despesa'] == 2017]

# Extraindo os valores

vals_2015 = ano_2015.groupby('mes_despesa')['vlr_despesa'].sum().values
vals_2016 = ano_2016.groupby('mes_despesa')['vlr_despesa'].sum().values
vals_2017 = ano_2017.groupby('mes_despesa')['vlr_despesa'].sum().values


meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Criando os gráficos
trace0 = go.Scatter(x = meses, 
                    y = vals_2015, 
                    name = '2015',
                    line = dict(
                       color = ('black'),
                       width = 4)
                   )

trace1 = go.Scatter(x = meses, 
                    y = vals_2016, 
                    name = '2016',
                    line = dict(
                        color = ('red'), 
                        width = 4)
                   )

trace2 = go.Scatter(x = meses,
                    y = vals_2017,
                    name = '2017',
                    line = dict(
                        color =('green'),
                        width = 4))

data = [trace0, trace1, trace2]

layout = dict(title = "Gastos cota parlamentar nos últimos 3 anos",
             yaxis = dict(title = 'Gastos'),
             xaxis = dict(title = 'Mes')) 

fig = dict(data=data, layout=layout)
iplot(fig, filename='Linhas')
    


# Observando o gráfico acima, parece haver um certo padrão de comportamento. Os gastos são sempre menores no início do ano e tem um pico em dezembro. O que explicaria esse padrão ? 
# 
# Aqui podemos responder nossa primeira questão. É claro que há uma tendência de alta nos gastos com cotas.

# ## Quais foram os parlamentares que mais consumiram recursos ? E quais foram os que menos consumiram recursos?
# 
# 
# Vamos descobrir quem são os paralamentares com maiores gastos.

# In[29]:


maiores_gastos = df_completo.groupby('nome_parlamentar')['vlr_despesa'].sum().sort_values(ascending=False).head(5)

plot_bar(maiores_gastos, "Os 5 Parlamentares com maior volume de gastos", "Parlamentar", "Gastos", "blue")


# Top 5 parlamentares que mais gastaram entre 2009 e 2017:
# 
# * Edio Lopes;
# * Wellington Roberto;
# * Silas Câmara;
# * Raimundo Gomes de Matos;
# * Gorete Pereira.

# ## Políticos que usaram menos valor das cotas paralamentares:

# In[30]:


menores_gastos = df_completo.groupby('nome_parlamentar')['vlr_despesa'].sum().sort_values().head()
                    

plot_bar(menores_gastos, "Os 5 parlamentares menos caros", "Parlamentar", "Gastos", "orange")


# * Athos Avelino;
# * João Fontes;
# * Ayrton Xerez;
# * Jusmari Oliveira;
# * Sebastião Madeira.
# 
# 
# ## Quais são as categorias de despesas mais onerosas dentre os recursos destinados às cotas parlamentares?
# 
# 

# In[31]:


cat_mais_caras = df_completo.groupby('desc_despesa')['vlr_despesa'].sum().sort_values(ascending=False)

plot_bar(cat_mais_caras, 'Gastos por categoria', 'Categoria', 'Gastos', "green")


# De longe divulgação da atividade parlamentar e passagens áreas lideram o volume de gastos. Quase 350 milhões de reais foram gastos com divulgação e 330 milhões com passagens aéreas. Outros valores também chamam atenção, como por exemplo 3 milhões com táxi e pedágio, locomoção e alimentação; quase 5.5M.

# No final da lista vemos 'participação em cursos, palestras...", ao meu ver são gastos referentes ao aprimoramento intelectual do parlamentar...é a categoria com menor gasto em 9 anos de dados observados, esse serviço representa menos de 400 mil dos gastos.
# 
# 
# Se os políticos não investem nem na própria educação, se preocupariam em investir em educação para o povo ? 
# 
# Não é de se estranhar que eles tenham aprovado [um corte de 50%](https://economia.estadao.com.br/noticias/geral,senado-aprova-corte-em-fundo-para-educacao,70002594632) dos recursos do pré-sal, destinados ao Fundo Social, que por sua vez é destinado a investimentos na educação e na saúde.

# ## Qual é o gasto por estado?

# In[32]:


gasto_por_estado = df_completo.groupby('uf')['vlr_despesa'].sum().sort_values(ascending=False)

plot_bar(gasto_por_estado, 'Gastos por estado', 'Estado', 'Gastos', 'pink')


# * São Paulo: 206M
# * Minas Gerais: 164M
# * Bahia: 129M
# * Rio de Janeiro: 128M
# * Rio Grande do Sul: 105M
# 
# 

# ## Qual estado tem maior número de representantes ?

# In[33]:


data = []
index = []
for i in pd.unique(df_completo.uf):
    index.append(i)
    data.append(len(pd.unique(df_completo[df_completo.uf == i ]['nome_parlamentar'])))   


# In[34]:


uf_maior_representatividade = pd.Series(data=data, index=index).sort_values(ascending = False)
plot_bar(uf_maior_representatividade, "UF's com mais representantes", "Qtd de parlamentateres", "Estados", 'red')


# * SP: 159
# * RJ: 110
# * MG: 103
# * BA: 84
# * RS: 65

# ## Quais partidos mais consomem a cota parlamentar ?

# In[35]:


piores_partidos = df_completo.groupby('partido')['vlr_despesa'].sum().sort_values(ascending=False)

plot_bar(piores_partidos, 'Gastos por Partido', 'Partido', 'Gastos', 'yellow')


# * PT: 230MM;
# * PP: 158MM;
# * PSDB: 150MM;
# * MDB: 136MM;
# * DEM: 121MM.

# ## Quais parlamentares tem a maior média de gastos?

# Neste ponto precisamos determinar uma quantidade mínima de vezes que o parlamentar aparece no dataset ou seja, a quantidade de vezes que ele solicitou reembolso. Arbitrariamente, irei considerar como valor mínimo cem vezes.

# In[36]:


count_parlamentares = df_completo['nome_parlamentar'].value_counts()


# In[37]:


# Criando uma função que retorne uma lista de parlamentares que usaram a cota, pelo menos mais de 100 vezes

def mais_de_cem(count_parlamentares):
    cem_mais = []
    for i in range(len(count_parlamentares)):        
        if count_parlamentares.values[i]>=100:
            cem_mais.append(count_parlamentares.index[i])
    return cem_mais


# In[38]:


politicos = df_completo[df_completo['nome_parlamentar'].isin(mais_de_cem(count_parlamentares)) == True]


# In[39]:


media_parlamentares = politicos.groupby('nome_parlamentar')['vlr_despesa'].mean().sort_values(ascending=False).head(5)
plot_bar(media_parlamentares, 'Parlamentares com maior média de gastos e que tenham usado a cota no mínimo 100x', 'Parlamentar',
         'Gasto médio', 'purple')


# * Armando Vergílio: 3600
# * Lucas Vergílio: 3043
# * Altineu Cortês: 2633
# * Marcos Antônio: 2492
# * Fernando Torres: 2296

# Neste ponto já temos algumas informações básicas do dataset. Já sabemos que o partido que mais gastou a cota parlamentar foi o PT, que SP é o estado com maior volume de gastos e o maior número de representantes, o parlamentar que mais gastou com cotas foi Édio Lopes enquanto Armando Vergílio possui a maior média de gastos.
# 
# Porém essas ainda são informações superficiais, agora podemos avaliar informações mais específicas, como por exemplo, o reemboldo de 215 mil reais. 

# In[40]:


df_completo['vlr_despesa'].max()


# In[41]:


df_completo[df_completo.vlr_despesa == 215000]


# Este gasto astronômico se deu em 12-2012, solicitado pelo deputado [Arnaldo Faria de Sá](https://pt.wikipedia.org/wiki/Arnaldo_Faria_de_S%C3%A1) que está em seu sétimo mandato. O serviço refere-se a divulgação de atividade parlamentar, que por sinal é a categoria mais onerosa dentre os gastos com cotas parlamentares.
# 
# A empresa beneficiária é BALCOLOR DIGITAL ATELIER GRAFICO LTDA, cujo dono é Maurício Artilheiro. 

# ***Vamos merguhar mais a fundo nos tipos de gastos. Vamos observar os gastos com alimentação.*** 
# 
# Vamos observar estes dados com base nos parlamentares que usaram a cota pelo menos 100 vezes.
# 
# ## Gastos com alimentação

# In[42]:


df_alimentacao = politicos[politicos['desc_despesa'] == 'FORNECIMENTO DE ALIMENTAÇÃO DO PARLAMENTAR']


# In[43]:


plt.figure(figsize = (15,8))

sns.boxplot(x=df_alimentacao['uf'], y=df_alimentacao['vlr_despesa'])
plt.title('Variação dos gastos com alimentação por UF');


# In[44]:


df_alimentacao.describe()


# A média de uma refeição de um parlamentar é de 65 reais trata-se de um valor bem alto. Através do gráfico **boxplot** podemos observar a distribução dos preços das refeições, temos uma quantidade bem considerável de refeições que custam mais de 1000 reais. Isso não faz nenhum sentido, se levarmos em conta que o salário mínimo sequer atingiu este valor. 
# 
# Em outras palavras, alguns políticos gastam am uma refeição mais que o valor do salário mínimo no Brasil.

# Vamos ver os parlamentares que mais gastaram com refeições, considerando a média.

# In[45]:


pols_maior_media_alimentacao = df_alimentacao.groupby('nome_parlamentar')['vlr_despesa'].mean().sort_values(ascending=False).head(5)

plot_bar(pols_maior_media_alimentacao, 'Top 5 políticos que mais gastaram com alimentação(média)', 'Político', 'Gastos')


# In[46]:


df_alimentacao[df_alimentacao.nome_parlamentar == 'MANOEL SALVIANO'].count()


# Manoel Salviano solicitou reembolsos referentes a alimentação 28 vezes. Como vimos, o valor médio de cada um desses reembolsos foi de mais de mil e setecentos reais. Se analisarmos por um outro ponto de vista, estes gastos seriam suficientes para pagar mais de um salarário mínimo para 28 trabalhadores. Ou pagar este mesmo salário para um trabalhador durante mais de dois anos. É no mínimo lamentável.

# In[47]:


df_alimentacao[df_alimentacao.vlr_despesa == 6205.0]


# Em outra breve visão, podemos ver que a "Liderança do PT" (Partido dos trabalhadores, maior partido brasileiro), gastou em uma única refeição seis mil duzentos e cinco reais, sim, em uma única refeição. Isso é mais do que muitos brasileiros que vivem abaixo da linha de pobreza gastam em um ano. 
# 
# Uma rápida pesquisa na internet, mostra que o restaurante não parece ser tão luxuoso a ponto de uma única refeição ter um custo tão alto (e mesmo que fosse, seria um absurdo). Então, o que teria acontecido para justificar tamnho gasto ? No meu ponto de vista, no mínimo houve algum tipo de confraternização ou banquete. Para aliados políticos ? Para colaboradores ? Será que de fato essa festa existiu ? E se existiu, é justificável tendo em vista a natureza para a qual é destinada o uso das cotas parlamentares ? 
# 
# E o pior de tudo, alguém sequer questiona isso ? Alguém audita esses absurdos ? Esse reembolso aconteceu em 2015...
# 

# In[48]:


restaurantes_mais_visitados = df_alimentacao.nome_fornecedor.value_counts().head(10)
plot_bar(restaurantes_mais_visitados, 'Top 10 restaurantes(ou não) favoritos dos políticos', "Restaurante", "Valor")


# Outro fato no mínimo curioso. Dentre os dez fornecedores de alimentação mais comuns, aparece o SENAC. Eu não sabia que eles serviam refeições.

# In[49]:


alimentacao_por_mes = df_alimentacao.groupby('mes_despesa')['vlr_despesa'].sum().sort_values(ascending=False)
plot_bar(alimentacao_por_mes, "Custo de Alimentação por mês", "Mês", "Valor")


# Os custos com alimentação tem seu pico em março e maio. 

# In[50]:


alimentacao_por_uf = df_alimentacao.groupby('uf')['vlr_despesa'].sum().sort_values(ascending=False)
plot_bar(alimentacao_por_uf, "Custo de Alimentação por UF", "UF", "Valor")


# Como de se esperar, os custos com alimentação por UF seguem o mesmo padrão dos gastos gerais. Exceto pelo "Sem informação", que ao contrário do padrão geral, aparece no início da lista.

# ## Fretamento de aeronvaves

# Mesmo tendo a sua disposição dinheiro para gastar com passagens aéres, alguns políticos preferem alugar seu próprio avião. No período de análise, mais de 14 milhões foram gastos com locação de aeronaves.
# 
# Quais foram os políticos que usaram nosso dinheiro para esse fim ?
# 

# In[51]:


df_aeronaves = df_completo[df_completo.desc_despesa == 'LOCAÇÃO OU FRETAMENTO DE AERONAVES']
df_aeronaves.shape


# In[52]:


df_aeronaves.head()


# In[53]:


df_aeronaves.describe()


# * A média do custo de uma aeronave fretada (táxi aéreo) para nossos políticos é de mais de 9 mil reais;
# * o custo máximo por esse serviço foi de mais de 180 mil reais;
# * 1638 foi a quantidade de vezes que este tipo de reembolso foi solicitado.

# In[54]:


politicos_voadores = df_aeronaves.nome_parlamentar.value_counts().sort_values(ascending=False).head(5)
plot_bar(politicos_voadores, "Políticos que mais usaram voos fretados", 'Politico', 'Quantidade')


# Átila Lins usou voos fretados nada menos que 98 vezes, seguido por Nilson Pinto, Francisco Chapinha, Ságuas Moraes e Júlio César.

# In[55]:


politicos_voadores_custo = df_aeronaves.groupby('nome_parlamentar')['vlr_despesa'].sum().sort_values(ascending=False).head(5)
plot_bar(politicos_voadores_custo, "Políticos que mais gastaram com voos fretados", 'Politico', 'Valor')


# Átila Lins também lidera o volume de gastos, mas dos cinco que mais utilizaram o serviço ( em quantidade ), três não aparecem na lista com maior volume de gastos. Eles são substituídos por três novos nomes: Paes Landin, Sabino Castelo Branco e Silas Câmara.

# In[56]:


empresas_voos = df_aeronaves.nome_fornecedor.value_counts().sort_values(ascending = False).head(5)
plot_bar(empresas_voos, "Empresas mais requisitadas", "Empresa", "Quantidade de vezes")


# In[57]:


df_aeronaves[df_aeronaves.vlr_despesa == 184500.000000]


# O senhor Sabino Castelo Branco é o detentor do reembolso com o maior valor referente à locação de aeronave. Representante do estado AM, do partido PTB. Não é de se surpreender que ele esteja entre os políticos que mais gastaram com este serviço.
# 
# Mas o que justifica estes gastos ? Será que eles são de estados onde não há aeroportos disponíveis ? Onde as empresas usuais não prestam serviços ? 

# In[58]:


df_aeronaves.uf.value_counts().sort_values(ascending=False).plot(kind='bar', title="Ranking dos políticos voadores por UF",
                                                                figsize=(12,8));


# Piauí possui três aeroportos, Pará também, Ceará nem se fala (trata-se de um dos estados mais visitados por turistas). 
# 
# Enfim, nesse brevee análise não identifiquei uma justificativa plausível para tamanho gasto. Embora, tenha que admitir que houve uma mudança considerável no ranking de gastos por estado se comparado ao ranking geral de gastos.

# # Conclusão
