
# coding: utf-8

# # Avaliação para Data Analyst - 99
# 
# Essa análise faz parte do processo de seleção para a vaga de data analyst na 99. A 99, antiga 99 Taxi, foi fundada em 2012 como um aplicativo para conectar passageiros a taxistas.
# 
# Graças a seu crescimento, a empresa recebeu investimentos milinários ao longo de 2017 , sendo finalmente adquirda pela gigante mundial de transporte privado, [Didi Chuxing](https://pt.wikipedia.org/wiki/Didi_Chuxing), em janeiro de 2018. Após essa aquisição, estima-se que a empresa fundada por por Paulo Veras, Renato Freitas e Ariel Lambrecht atingiu o valor de mercado de US$1 Bilhão se tornando a primeira "unicórnio" brasileira. 
# 
# ## O exercício
# 
# O exercício propõe a realização de uma análise sobre as despesas com cotas parlamentares do congresso nacional no período de 2009 à 2017. 
# 
# Os dados utilizados foram extraídos do portal [dos dados abertos](http://www2.camara.leg.br/transparencia/cota-para-exercicio-da-atividade-parlamentar/dados-abertos-cota-parlamentar) da câmara federal. Aqui também pode ser acessada a descrição dos [dados](http://www2.camara.leg.br/transparencia/cota-para-exercicio-da-atividade-parlamentar/explicacoes-sobre-o-formato-dos-arquivos-xml).
# 
# O exercício se divide em duas partes:
# 
#    
# ### 1ª parte: 
# 
# **Fazendo uso de gráficos, tabelas e/ou métricas estatísticas, responder as seguintes questões:**
# 
# a. Como se comportam os gastos com cotas parlamentares ao longo do tempo? Existe alguma tendência de aumento ou redução desse custo? Existe sazonalidade?
# 
# b. Quais foram os parlamentares que mais consumiram recursos durante o mandato 2011-2014? E
# quais foram os que menos consumiram recursos?
# 
# c. Quais são as categorias de despesas mais onerosas dentre os recursos destinados às cotas
# parlamentares?
# 
# d. Qual é o custo per capita de um parlamentar em cada unidade da federação? (considerando
# somente as despesas de cota parlamentar)
# 
# 
# ### 2ª parte:
# 
# **Essa parte é livre, ficando a cargo do candidato realizar análises e responder suas próprias questões.**
# 
# Neste caso, responderei as seguintes questões:
# 
# a. Qual partido mais consumiu recursos ? 
# 
# b. Qual candidato gastou mais em combustível no período x ?
# 
# 
# 
# # O trabalho será dividido nas seguintes sessões:
# 
# ### 1. Carga, limpeza e transformação dos dados:
# 
# Nessa etapa irei explorar o conjunto de dados em busca de anomalias que precisam ser tratadas para viabilizar a devida análise. Isso envolve detectar valores ausentes, corrigir o formato de dados armazenados de forma incorreta e criar e/ou transformar os dados a partir dos atributos existentes. 
# 
# ### 2. Análise exploratória
# 
# Aqui buscaremos as respostas para as questões realizadas, bem como descobrir novos questionamentos que possam nos direcionar a descobertas significantes.
# 
# ### 3. Conclusão
# 
# Nessa seção demonstrarei as conclusões da análise e compartilharei os ***insghts*** descobertos, bem como novas possíveis linhas de análise.
# 

# ## 1. Carga, limpeza e transformação dos dados

# Importanto as bibliotecas necessárias para a análise e carregando os dados.

# In[1]:


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


# Após avaliar os atributos dos datasets, abaixo segue uma breve descrição de cada coluna, bem como quais serão mantidas e excluídas. Sempre levando em conta o objetivo da análise.
# 
# * 0 txNomeParlamentar - Nome do parlamentar - manter pois é útil para responder a primeira questão proposta;
# * 1 idecadastro - Id do parlamentar - excluir - trata-se apenas de um código, nesse momento pode não ser relevantes;
# * 2 nuCarteiraParlamentar - Documento do parlamentar - excluir - mais um código;
# * 3 nuLegislatura - Ano início da legislatura do parlamentar - manter 
# * 4 sgUF - manter
# * 5 sgPartido manter
# * 6 codLegislatura numero da legislatura - excluir
# * 7 numSubCota - Cod tipo de despesa - excluir - para nossa análise, a descrição é mais importante do que o código;
# * 8 txtDescricao - Descrição do tipo de despesa - manter
# * 9 numEspecificacaoSubCota - especificação detalhada da despesa código - excluir
# * 10 txtDescricaoEspecificacao - descrição detalhada da despesa - manter
# * 12 txtCNPJCPF - cpf ou cnpj do fornecedor do serviço - excluir
# * 11 txtFornecedor - nome do fornecedor do serviço - manter
# * 13 txtNumero - numero do doc fiscal - excluir
# * 14 indTipoDocumento - nf ou recibo - excluir
# * 15 datEmissao - data Emissão da nota ou doc fiscal - manter
# * 16 vlrDocumento - valor da despesa e pode ter valores negativos - excluir 
# * 17 vlrGlosa - Também representa custo do serviço - excluir
# * 18 vlrLiquido  - O valor final da despesa, o que de fato será debitado da cota
# do parlamentar - manter
# * 19 numMes - mes - manter
# * 20 numAno - ano - manter
# * 21 numParcela - quando o parlamentar recebe um reembolso de forma parcelada - excluir
# * 22 txtPassageiro - Nome do passageiro, quando a despesa for relacionada a 
# passagens aérea - manter
# * 23 txtTrecho - trecho da viagem - manter
# * 24 numLote - utilizado para localizar os documentos - excluir
# * 25 numRessarcimento - idem - excluir
# * 26 vlrRestituicao - esse valor pode ser descontado do valor do documento,
# como o valor do documento compõe o vlr liquido e nós excluimos o valor do doc, Não
# há necessidade de manter essa coluna.
# * 27 nuDeputadoId - excluir
# * 28 ideDocumento - excluir

# Carga dos dados

# In[2]:


anos = range(2009,2018) # Até 2018, pois range exclui o último valor

# Lista com as colunas que serão mantidas para análise
colunas = ['txNomeParlamentar', 'nuLegislatura', 'sgUF', 'sgPartido', 'codLegislatura','txtDescricao', 'txtDescricaoEspecificacao',
          'txtFornecedor', 'datEmissao', 'vlrLiquido', 'numMes', 'numAno', 'txtPassageiro', 'txtTrecho']

dfs = []

for ano in anos:
    df = pd.read_csv('Ano-{}.csv'.format(ano), sep=';', error_bad_lines=True, usecols=colunas,  index_col=False, dtype='unicode')
    dfs.append(df)
    df_completo = pd.concat(dfs, ignore_index=True)
    


# In[3]:


df_completo.to_csv('df_completo.csv')


# In[4]:


df_completo.head()


# In[5]:


df_completo.tail()


# In[6]:


df_completo.isnull().sum()


# In[7]:


df_completo.info()


# Agora que os dados foram carregados, iniciaremos o processo de tratamento dos dados. Como vimos todos os dados estão com o formato de 'object'. Isso aconteceu pois especifiquei que o dataset teria apenas um tipo de dado através do parâmetro `dtype` no momento de importá-lo. Isso foi necessário devido ao tamanho do dataset (mais de 3MM de linhas), o pandas reconhece o tipo de dados de cada coluna apenas após percorre-la por completo. Essa tarefa neste dataset exije muita performance de memória e está sujeito a erros, por isso, especifiquei um único formato para todo o dataset, livrando o pandas dessa tarefa.
# 
# 

# ## Tranformações a serem realizadas
# 
# **Valores ausentes:**
# 
# **nuLegislatura:** Temos apenas 7 valores nulos, irei excluir essas linhas, acredito que esse número não irá prejudicar a análise.
# 
# **sgUF** e **sgPartido**: 3786 valores nulos, irei usar a mesma abordagem, tendo em vista que esse número representam nem 1% do volume total dos dados;
# 
# **txtDescricaoEspecificacao**: Conforme a descrição dos dados, essa coluna trata-se de uma descrição mais detalhada de algum serviço e essa descrição só é necessária em alguns casos. Portanto, é de se esperar um considerável volume de dados ausesntes. Irei preencher os valores nulos com "Sem Detalhamento".
# 
# **datEmissao**: Através dessa coluna, podemos extrair o dia da semana. Assumindo que a data da nota é a data que o serviço foi prestado, podemos extrair algumas informações interessantes. Entretanto ela tem 44 mil valores nulos, vamos ver como iremos tratá-los.
# 
# **txtPassageiro** e **txtPassageiro**: Similar a coluna **txtDescricaoEspecificacao** só é preenchida quando o serviço prestado se trata de passagem aérea, pode ser interessante descobrir quais parlamentares mais usam este serviço, por isso irei manter essa coluna e os dados ausentes serão preenchidos com a informação 'Não é Serviço de voo'.
# 
# 
# **Formatação dos dados**:
# 
# Todos os dados estão no formato `object`o que é um problema. Nem todas as colunas devem armazenar dados neste formato. Seguem as colunas que devem sofrer alterações:
# 
# **vlrLiquido**: Tranformar este dados em `float`, tendo em vista que trata-se de dinheiro.
# 
# **numMes** e **numAno**: Transformar em `int`.

# ### Preparação dos dados 
# 
# #### Valores ausentes
# 

# **txtDescricaoEspecificacao**

# In[8]:


df_completo.txtDescricaoEspecificacao.value_counts()


# Ops ! Parece que um valor similar já existe na coluna, por que nem todos estão preenchidos ?
# 
# Vamos filtrar e entender melhor estes dados. Vamos selecionar as linhas do dataset apenas onde o valor de txt.DescricaoEspecificacao esteja nulo:

# In[9]:


dados_ausentes_descricao = df_completo[df_completo['txtDescricaoEspecificacao'].isnull() == True]


# In[10]:


dados_ausentes_descricao.shape


# Analisando as primeiras linhas para entender a relação com as demais colunas...

# In[11]:


dados_ausentes_descricao.head()


# Quais são os gastos quando não há velores na txtDescricaoEspecificacao ?

# In[12]:


dados_ausentes_descricao.txtDescricao.value_counts()


# Ao que parece o único gasto ausente é com combustível...
# 
# Selecionando as linhas preenchidas:

# In[13]:


dados_preenchidos = df_completo[df_completo['txtDescricaoEspecificacao'].isnull() == False]
dados_preenchidos.head()


# In[14]:


dados_preenchidos.txtDescricao.value_counts()


# Aqui, somente os gastos relativos à combustível...

# In[15]:


df_completo[df_completo['txtDescricaoEspecificacao']== 'Aeronaves'].head()


# In[16]:


df_completo[df_completo['txtDescricaoEspecificacao']== 'Embarcações'].head()


# In[17]:


df_completo[df_completo['txtDescricaoEspecificacao']== 'Sem especificações'].head()


# In[18]:


len(df_completo[df_completo['txtDescricao']== 'COMBUSTÍVEIS E LUBRIFICANTES.']) == len(dados_preenchidos)


# **Conclusão:** 
# A coluna **txtDescricaoEspecificacao** só é preenchida quando o parlamentar faz uso de sua verba para aquisição de combustíveis. O número de vezes que a descrição 'COMBUSTÍVEIS E LUBRIFICANTES.' aparece na coluna **txtDescricao** é o mesmo número de células preenchidas na **txtDescricaoEspecificacao**.
# 
# A descrição 'Sem especificações' é um valor válido, pois refere-se ao uso de serviços de lubrificantes e combustíveis, mas sem a especificação do veículo utilizado. Portanto, este valor representa uma informação diferente da que pensamos em usar para preencher os valores ausentes, então podemos seguir com essa abordagem, mas mudando um pouco o dado que será inserido.

# In[19]:


df_completo.txtDescricaoEspecificacao.fillna('Não há necessidade de especificação', inplace=True)


# In[20]:


df_completo.txtDescricaoEspecificacao.isnull().sum()


# **txtPassageiro** e **txtTrecho**

# In[21]:


df_completo.txtPassageiro.value_counts().head()


# In[22]:


df_completo.txtTrecho.value_counts().head(10)


# Filtrando os dados onde as linhas de txtTrecho estejam vazias...

# In[23]:


voos = df_completo[df_completo['txtTrecho'].isnull() == False ]


# In[24]:


voos.head()


# In[25]:


voos.txtDescricao.value_counts()


# A coluna **txtTrecho** é uma coluna com dados de qualidade muito ruim. Portanto, pensando nas perguntas que preciso responder, excluiremos a coluna. 

# In[26]:


df_completo.drop('txtTrecho', axis=1, inplace=True)


# In[27]:


df_completo.columns


# Já em relação à coluna **txtPassageiro**, vamos preencher os valores ausentes.

# In[28]:


df_completo.txtPassageiro.fillna('Não é Serviço de voo', inplace=True)
df_completo.txtPassageiro.isnull().sum()


# Vamos avaliar os dados ausentes do campo data emissão: 

# In[29]:


sem_data_emissao = df_completo[df_completo['datEmissao'].isnull() == True]
sem_data_emissao.head()


# In[30]:


sem_data_emissao.numAno.value_counts()


# Para decidir se a melhor abordagem é excluir as linhas sem registros, vamos verificar quanto as linhas sem registro na data de emissão, representam do total de observações:

# In[31]:


perc = 44454 / df_completo.shape[0] * 100

perc


# As 44mil linhas representam pouco mais de 1% do dataset. Excluir essas observações não impactará em nossa análise. Somados a mais 3786 linhas das colunas sgUF e sgPartido, não chegamos nem a 2% do conjunto de dados. 
# 
# Dessa forma, considero mais prático excluir todas essas linhas com valores ausentes.

# In[32]:


df_completo.isnull().sum()


# In[33]:


df_completo.dropna(inplace = True)


# In[34]:


df_completo.isnull().sum()


# In[35]:


df_completo.shape


# Não temos mais valors nulos em nosso conjunto de dados e sacrificamos apenas 1,55% dos nossos dados.

# ### Transformação e formatação dos dados
# Agora podemos seguir para a fase de transformação dos dados. Aqui além de corrigir os formatos de dados incosistentes, iremos criar e incluir novas variáveis. 

# #### Convertendo os valores da colunas vlrLiquido

# In[36]:


valor = df_completo.vlrLiquido
valor = [float(x.replace(',','.')) for x in valor ] # Usando um loop para converter um valor por vez...


# Convertendo a lista de strings para uma série do pandas para recolocar no dataset o valor convertido para float.

# In[37]:


valor = pd.Series(valor)
df_completo['vlrLiquido'] = valor
df_completo.info()


# Dado convertido com sucesso ! 

# #### Convertendo os valores de data de emissão
# 
# Vamos converter para `datetime`. 

# In[38]:


dt_emissao = df_completo.datEmissao

datas = [x.split(' ')[0] for x in dt_emissao]

datas[:5]


# Muitos dados não fazem sentido na coluna datEmissao. Podemos observar valor de anos como 2209, 5009.
# 
# Irei limpar os dados, seguindo a lógica de que qq nota com ano superior à 2017 será assumido o ano de 2017. E anos que forem menores à 2009, serão padronizados para 2009.

# In[39]:


# Separando em partes

ano = [x.split('-')[0] for x in datas]
mes = [x.split('-')[1] for x in datas]
dia = [x.split('-')[2] for x in datas]


# In[40]:


ano = [2017 if int(x) > 2017 else x for x in ano ]


# In[41]:


ano_corrigido = [2009 if int(x) < 2009 else x for x in ano ]


# In[42]:


pd.Series(ano_corrigido).unique()


# In[43]:


# Juntando as datas novamente

nova_dt_emissao = []

for i in range(len(ano_corrigido)):
    data = str(ano_corrigido[i]) + '-' +  str(mes[i]) + '-' + str(dia[i])
    nova_dt_emissao.append(data)


# In[44]:


nova_dt_emissao[:10]


# Transformamos as strings da lista datas em objetos datetime, graças ao uso do módulo `datetime`. Agora para extrair os dias da semana dessas datas usarei a função `isoweekday()` do módulo datetime.
# 
# Ela devolverá uma lista com os seguintes valores:
# 
# * 1 = Segunda;
# * 2 = Terça;
# * 3 = Quarta;
# * 4 = Quinta;
# * 5 = Sexta;
# * 6 = Sábado;
# * 7 = Domingo.
# 
# 
# 
# 

# In[45]:


semana = [datetime.strptime(x, '%Y-%m-%d') for x in nova_dt_emissao]
semana = [x.isoweekday() for x in semana]


# Agora, preciso converter estes números em dias da semana, para facilitar a leitura e análise. Criarei uma função para fazer esse trabalho:

# In[46]:


def dias_da_semana(semana):
    
    ''' Retorna uma lista de strings com os dias da semana
    
    Parâmetros
    
    semana: lista ou pdSeries com os valores numericos que representam cada dia da semana
    
    '''
    
    dias_escritos = []    
    for i in semana:
        if i == 1:
            dia =  'segunda-feira'
            dias_escritos.append(dia)
        elif i == 2:
            dia = 'terça-feira'
            dias_escritos.append(dia)
        elif i == 3:
            dia = 'quarta-feira'
            dias_escritos.append(dia)
        elif i == 4:
            dia = 'quinta-feira'
            dias_escritos.append(dia)
        elif i == 5:
            dia = 'sexta-feira'
            dias_escritos.append(dia)
        elif i == 6:
            dia = 'sábado'
            dias_escritos.append(dia)
        else:
            dia = 'domingo'
            dias_escritos.append(dia)
        
    
    
    return dias_escritos


# In[47]:


semana = dias_da_semana(semana=semana)


# In[48]:


df_completo['dia_semana'] = semana


# In[49]:


df_completo['datEmissao'] = nova_dt_emissao


# In[50]:


df_completo[['dia_semana', 'datEmissao']].head(20)


# Ok, agora temos uma nova dimensão no dataset ! 
# 
# Vamos trabalhar no mês e ano.

# Vamos converter as colunas 'numAno' e 'numMes' para `int`.

# In[51]:


df_completo['numMes'] = df_completo['numMes'].astype(int) 


# In[52]:


df_completo['numMes'].dtypes


# In[53]:


df_completo['numAno'] = df_completo['numAno'].astype(int)
df_completo['numAno'].dtypes


# In[54]:


df_completo.info()


# In[55]:


df_completo['nuLegislatura'] = df_completo.nuLegislatura.astype(int)


# ## Análise Exploratória
# 
# Agora que os dados estão limpos e preparados, podemos iniciar a nossa exploração e buscar responder as perguntas feiras no enunciado.

# In[56]:


df_completo.describe(include='all').round()


# Com base neste quadro de resumo, já conseguimos ver algumas informações interessantes rapidamete. Por exemplo:
# 
# * A média de gastos, considerando o período de 2009 à 2017 é de 535 reais. Isso quer dizer que cada vez que um político usa sua cota parlamentar, ele gasta em média mais de 500 reais;
# 
# * O maior reembolso/pagamento foi de 215 mil reais;
# 
# * Mais de 50% das despesas custam mais de 124 reais; 
# 
# * A despesa mais comum é o reembolso de bilhetes / passagens aéreas;
# 
# * Vanderlei Macris é o político mais utilizou a cota parlamentar.
# 
# Esse é um breve resumo de algumas características do dataset.

# **1 - Como se comportam os gastos com cotas parlamentares ao longo do tempo? Existe alguma
# tendência de aumento ou redução desse custo? Existe sazonalidade?**
# 
# Vamos entender como os gastos com cotas parlamentares evoluíram ao longo do tempo. Vamos começar verificando o gasto médio mensal, por ano. 
# 
# Ou seja, computaremos a soma de todos os gastos por ano e dividiremos cada resultado por 12. Isso nos dará um valor médio mensal de gastos em cada ano. 
# 
# Acredito que o comportamente dessa média ao longo dos anos, pode nos ajudar a identificar tendências de aumento ou queda dos gastos com nossos políticos.

# In[59]:


# calculando medias anuais 
gastos_media_mensal = df_completo.pivot_table('vlrLiquido', index= 'numAno', aggfunc='sum')
gastos_media_mensal = round(gastos_media_mensal/12)


# In[61]:


gastos_media_mensal


# In[63]:


gastos_media_mensal.plot(title='Evolução média mensal de gastos com cotas parlmentares - 2009 à 2017', figsize=(15,5), 
                        linestyle='--', color = 'blue')

plt.ylabel('Média Anual de Gastos');


# * A média mensal mostra com clareza que, a cada ano que passa, gastamos mais com nossos parlamentares;
# 
# * Em 2009 as cotas parlamentares registravam um valor mensal médio de aproximadamente 9.6 milhões contra mais de 18 milhões em 2016, ano em que este valor foi mais alto;
# 
# * Comparando estes dois períodos o crescimento foi de quase 300% ! 

# In[64]:


df_completo.groupby('numAno')['vlrLiquido'].sum().round()


# In[65]:


df_completo.groupby('numAno')['vlrLiquido'].sum().plot(kind='bar', figsize=(15,5), title="Valor anual de gastos", 
                                                      rot=45)
plt.ylabel('Total Gastos');


# * O gráfico acima, só reforça a nossa suspeita de que os gastos estão em uma forte tendência de alta;
# 
# * Em 2016 os gastos atingiram 222 milhões. O crescimento em relação à 2009 foi de 93%; 
# 
# * A crescente nos gastos ocorreu mesmo entre os anos de 2015 e 2016, período em que o Brasil esteve mergulhado em uma de suas maiores recesssões, tendo quedas consecutivas no PIB, sendo 3,8% e 3,6% em 2015 e 2016 respectivamente; 
# 
# * Mesmo a [pior crise desde 1945](http://g1.globo.com/jornal-hoje/noticia/2017/03/brasil-vive-pior-recessao-da-historia.html), não foi capaz de frear a subida dos gastos com a classe política;
# 
# 

# **Será que o aumento dos gastos tem a ver com a quantidade de políticos ?**

# In[66]:


politicos_09 = len(df_completo[df_completo['numAno'] == 2009]['txNomeParlamentar'].unique())
politicos_16 = len(df_completo[df_completo['numAno'] == 2016]['txNomeParlamentar'].unique())


print("A quantidade de parlamentares em 2009 era de {}.".format(politicos_09))
print('\n')
print("A quantidade de parlamentares em 2016 era de {}.".format(politicos_16))


# Será que o aumento de 4% na quantidade de parlamentares, justifica o aumento de 93% nos gastos ? Eu acredito que não.

# In[67]:


total_gastos_mes = df_completo.pivot_table('vlrLiquido', index= 'numMes', aggfunc='sum', columns='numAno', margins=False).round()
total_gastos_mes


# A tabela acima, apresenta a evolução dos gastos parlamentares por mês. Espero que essa divisão nos ajude a encontrar possíveis sazonalidades.
# 
# Para isso, vamos plotar um gráfico por ano.

# In[68]:


total_gastos_mes.plot(subplots=True, figsize=(15,15), sharey=True, title='Evolução gastos mensais', linestyle='--', fontsize=10)
plt.ylabel('Total gastos por mês');


# Observando os gráficos podemos concluir que há **sazonalidade**. 
# 
# Ela ocorre entre os meses de **agosto** e **dezembro**. Os gastos diminuem neste período e voltam a crescer à partir de **fevereiro** ate o meio do mês de **março**, ficando relativamente estáveis até agosto quando voltam a cair. Esse padrão é explicado pelo [recesso parlamentar](http://www2.camara.leg.br/comunicacao/assessoria-de-imprensa/recesso-dos-deputados) que começa em 1º de agosto e termina em 22 de dezembro. A elevação dos gastos a partir de fevereiro marca o retorno das sessões legislativas, que seguem de 2 de fevereiro até 17 julho.
# 
# As exceções ocorrem em 2010 e 2014, período de eleções. Vamos olhar mais de perto.

# In[69]:


eleicao_2010 = df_completo[df_completo['numAno'] == 2010]
eleicao_2011 = df_completo[df_completo['numAno'] == 2011]

eleicao_2014 = df_completo[df_completo['numAno'] == 2014]
eleicao_2015 = df_completo[df_completo['numAno'] == 2015]


# In[70]:


eleicao_2010_agrupado = eleicao_2010.groupby('numMes')['vlrLiquido'].sum()
eleicao_2011_agrupado = eleicao_2011.groupby('numMes')['vlrLiquido'].sum()
eleicao_2014_agrupado = eleicao_2014.groupby('numMes')['vlrLiquido'].sum()
eleicao_2015_agrupado = eleicao_2015.groupby('numMes')['vlrLiquido'].sum()


# In[71]:




fig, axes = plt.subplots(2,2, sharex=True, sharey=True, figsize=(15,8))



ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

ax1.plot(eleicao_2010_agrupado)
ax2.plot(eleicao_2014_agrupado)
ax3.plot(eleicao_2011_agrupado)
ax4.plot(eleicao_2015_agrupado)


ax1.set_title('Eleição de 2010')
ax2.set_title('Eleição de 2014')
ax3.set_title('2011 Pós eleição')
ax4.set_title('2015 Pós eleição');


# Olhando mais de perto fica ainda mais claro a mundança do padrão dos gastos paralamentares em anos de eleição. Eu diria que por volta de abril, os parlamentares já começam a botar em prática suas estratégias para se manterem em seus cargos isso explica a queda dos gastos e em agosto, saem em campanha fazendo o movimento totalmente contrário em relação aos outros anos.
# 
# 
# Acredito que essas análises respondem a nossa primeira pergunta. 

# **2 - Quais foram os parlamentares que mais consumiram recursos durante o mandato 2011-2014? E
# quais foram os que menos consumiram recursos?**
# 
# **Quero nomes !**
# 
# Vamos descobrir quem são os paralamentares com maiores gastos entre os período de 2011 e 2014. 
# 
# Criaremos um dataset reduzido para essa análise. Como temos mais de 500 paralamentares, vamos focar apenas nos 20 parlamentares que gastaram mais dos 10 partidos mais representativos no período de 2011 à 2014. 

# In[72]:


# Criando um dataset somente com os anos de 2011 até 2014.

df_mandato = df_completo[df_completo['numAno'].isin([2011,2012,2013,2014])]
df_mandato.head()


# In[74]:


df_mandato.shape


# In[75]:


# focando nos principais parlamentares partidos
df_mandato.sgPartido.value_counts(ascending=False).head(10)


# Estes são os dez partidos com maior expressividade no dataset entre 2011 e 2014, vamos focar a análise nestes partidos.

# In[76]:


top_dez_partidos = ['PT', 'PP','PSDB','MDB','PR','PSD','DEM','PMDB','PSB','PCdoB'] 
                    
                    
                    
df_mandato = df_mandato[df_mandato['sgPartido'].isin(top_dez_partidos)]

df_mandato.shape


# In[77]:


df_mandato.head()


# Agora, vamos descobrir os políticos gastões!
# 
# Vamos ver os 20 primeiros da lista:

# In[78]:


pd.DataFrame(df_mandato.groupby(['txNomeParlamentar', 'sgPartido', 'sgUF'],)['vlrLiquido'].sum().sort_values(ascending=False)).head(20)


# Considerando os dez partidos com maior expressividade, em primeiro lugar temos [Henrique Fontana](http://www2.camara.leg.br/deputados/pesquisa/layouts_deputados_biografia?pk=73482) do PT. Filiado ao Partido dos Trabalhadores desde 1984, este médico de natural de  Porto Alegre-RS está em seu quinto mandato como deputado federal. De acordo com a [lei da cota parlamentar](http://www2.camara.leg.br/transparencia/acesso-a-informacao/copy_of_perguntas-frequentes/cota-para-o-exercicio-da-atividade-parlamentar), ele teria direito a gastar 40.875 reais por mês. 
# 
# ![Henrique Fontana](https://ptnacamara.org.br/portal/wp-content/uploads/2015/05/HenriqueFontana-225x300.jpg)
# 
# Calculando seu gasto médio mensal entre 2011 e 2014 foi de 63 mil reais, bem acima da sua cota mensal. Com o que ele gasta, tanto dinheiro ? 
# 
# 
# 

# In[79]:


df_mandato[df_mandato['txNomeParlamentar'] == 'HENRIQUE FONTANA']['txtDescricao'].value_counts().plot(kind='barh',
                                                                                                     figsize=(10,10), title='Gastos Dep. Henrique Fontana');


# A maior número de pedidos de cota para o senhor Henrique fontana é referente locação de veículos e fretamento de embarcações. Isso não quer dizer que esse seja seu maior gasto, vamos ver:

# In[80]:


df_fontana = df_mandato[df_mandato['txNomeParlamentar'] == 'HENRIQUE FONTANA']

df_fontana.groupby('txtDescricao')['vlrLiquido'].sum().sort_values(ascending=False).plot(kind='barh',
                                                                                                     figsize=(10,10), title='Gastos Dep. Henrique Fontana');


# Embora o maior numero de pedidos de reembolso sejam referentes a locações e embarcações, o maior volume de gastos do deputado, está relacionado à passagens aéreas. Como a grande maioria.
# 
# Além de Henrique Fontana, entre os gastões temos outros ilustres políticos como o sr [João Pizzolati](https://g1.globo.com/sc/santa-catarina/noticia/2018/09/27/mpsc-pede-prisao-de-ex-deputado-joao-pizzolatti-por-descumprir-medida-judicial.ghtml), que se envolveu em um grave acidente de carro no final de 2017, foi punido com uma medida cautelar e teve a prisão solicitada pelo Ministério Público de Santa Catarina, após descumprimento dessa medida. Um exemplo de cidadão !
# 
# 
# 
# 
# Agora vamos ver os deputados que menos gastam.

# In[81]:


pd.DataFrame(df_mandato.groupby([ 'sgPartido','txNomeParlamentar','sgUF'],)['vlrLiquido'].sum().sort_values(ascending=True)).head(20)


# O senador [Eunício Oliveira](https://pt.wikipedia.org/wiki/Eun%C3%ADcio_Oliveira) do PMDB é o político com menor gasto no período de 2011 â 2014. Atualmente o cearense de Lavras da Mangabeira, preside o Senado Federal, sucessedendo Renan Calheiros desde 1º de fevereiro de 2017. 
# 
# ![Eunicio de Oliveira](http://www.aesquerdadiario.com/IMG/arton15596.jpg)
# 
# Boa Eunício...mas também com um salário de mais de 30mil, 13º, 14º e 15º, trabalhando apenas três vezes por semana e podendo votar o próprio aumento. Não precisa ser nenhum economista para economizar com as cotas, né ? 
# 
# Difícil mesmo é se virar o mes todo com um salário mínimo de menos de 1000 reais...
# 
# A lista dos poupadores também conta com nomes famosos, como [Antonio Palocci](https://pt.wikipedia.org/wiki/Antonio_Palocci), condenado a 12 anos de prisão na Lava Jato, pelo juiz Sérgio Moro em junho de 2017... 

# **3 - Quais são as categorias de despesas mais onerosas dentre os recursos destinados às cotas
# parlamentares?**
# 
# Vamos mergulhar um pouco nas categorias dos gastos. Aqui teremos que fazer uma melhoria no dataset, vimos que temos duas nomenclaturas para gastos com passagens aéres, vamos corrigir isso. Vamos criar uma variante do dataset `df_mandato`, dessa vez considerando todos os mandatos.

# In[82]:



df_mandato_geral = df_completo[df_completo['sgPartido'].isin(top_dez_partidos)]

df_mandato_geral['txtDescricao'].value_counts()


# In[83]:


descricao = df_mandato_geral['txtDescricao']

descricao = descricao.replace('Emissão Bilhete Aéreo', 'PASSAGENS AÉREAS')

# Agrupando a locação de veículos e embarcações em uma só categoria 

descricao = descricao.replace(['LOCAÇÃO DE VEÍCULOS AUTOMOTORES OU FRETAMENTO DE EMBARCAÇÕES', 'LOCAÇÃO OU FRETAMENTO DE EMBARCAÇÕES'], 
                              'LOCAÇÃO DE VEÍCULOS AUTO OU EMBARCAÇOES' )

descricao.value_counts()


# In[84]:


df_mandato_geral['txtDescricao'] = descricao

df_mandato_geral.groupby('txtDescricao')['vlrLiquido'].sum(normalize=True).sort_values(ascending=False).round().plot(kind='bar', figsize=(15,5),
                                                                                                 title='Gastos Gerais por Categoria')

plt.ylabel('Gastos');


# Passagens aéreas lideram as categorias mais onerosas, seguido por combustível, telefonia e serviços postais. É um pouco curioso serviços postais figurarem entre os maiores gastos, na era da informação. 
# 
# A lista é encabeçada por gastos referentes a locomoção e comunicação.
# 
# No final da lista vemos 'participação em cursos, palestras...", ao meu ver são gastos referentes ao aprimoramento intelectual do parlamentar...é a categoria com menor gasto. 
# 
# 
# Se os políticos não investem nem na própria educação, se preocupariam em investir em educação para o povo ? 
# 
# Não é de se estranhar que eles tenham aprovado [um corte de 50%](https://economia.estadao.com.br/noticias/geral,senado-aprova-corte-em-fundo-para-educacao,70002594632) dos recursos do pré-sal, destinados ao Fundo Social, destinado a investimentos na educação e na saúde, agora em 8 de dezembro.

# In[85]:


pd.DataFrame(df_mandato_geral.pivot_table('vlrLiquido', index='txtDescricao', columns='numAno', aggfunc='mean'
                             ,margins=True).round())


# O gasto médio com combustíveis continua crescendo ano após ano, mesmo em 2017 não houve queda neste gasto, como aconteceu no geral. Telefonia também mantem a crescente, fornecimento de alimentação ao parlamentar, também cresceu bastante.
# 
# A comida deve ser maravilhos nos restaurantes em que uma refeição custa em média 600 reais

# **4 - Qual é o custo per capita de um parlamentar em cada unidade da federação? (considerando
# somente as despesas de cota parlamentar)**
# 
# Afinal, quanto isso tudo custa para cada cidadão ??

# In[86]:


populacao = pd.read_csv('brasilpop.csv')


# In[87]:


populacao.head()


# In[88]:


df_mandato_geral = pd.merge(df_mandato_geral,populacao, left_on='sgUF', right_on='UF')


# In[89]:


df_mandato_geral.head()


# In[90]:


df_mandato_geral.pivot_table('vlrLiquido', index='numAno', columns='sgUF', margins=True )


# In[91]:


df_mandato_geral.groupby(['sgUF','numAno']).sum().round()


# In[94]:


gastos_totais_por_uf = df_mandato_geral.groupby(['sgUF'])['vlrLiquido'].sum().sort_values(ascending=False).round()


# In[95]:


gastos_totais_por_uf.plot(kind='barh', figsize= (10,10), title='Gastos acumulados por UF')
plt.ylabel('UF')
plt.xlabel('Gastos');


# São Paulo, Minas Gerais e Rio Grande do Sul lideram o valor acumulado de gastos com cotas. Vamos ver se seus cidadão são os que pagam mais caro por seus políticos.
# 
# Vamos calcular o custo médio per capita. Para isso criarei um mini dataset.

# In[119]:


pop = df_mandato_geral.groupby('POP EST') # Criando a variavel populacao


# In[97]:


pop


# In[98]:


gastos_totais_por_uf = pd.DataFrame(gastos_totais_por_uf)


# In[99]:


gastos_totais_por_uf.index


# In[100]:


gastos_totais_por_uf.reset_index(inplace=True)


# In[101]:


gastos_totais_por_uf.info()


# In[102]:


gastos_totais_por_uf_pop = pd.merge(gastos_totais_por_uf, populacao, left_on='sgUF', right_on='UF') 


# In[103]:


gastos_totais_por_uf_pop


# In[104]:


gastos_totais_por_uf_pop['media_per_capita'] = gastos_totais_por_uf_pop['vlrLiquido']/gastos_totais_por_uf_pop['POP EST']


# In[105]:


gastos_totais_por_uf_pop


# In[106]:


gastos_totais_por_uf_pop = gastos_totais_por_uf_pop.round().sort_values(by='media_per_capita')


# In[107]:


gastos_totais_por_uf_pop.set_index('Und Fed', inplace=True)
gastos_totais_por_uf_pop.media_per_capita.plot(kind='bar', figsize=(15,8), title= 'Custo dos Parlamentares - Per Capita');


# Os três estados onde o valor per capita de um parlamentar é mais alto, tem menos de um milhão de habitantes. Embora o numero de habitantes do estado pelo qual o parlamentar foi eleito seja usado para calcular sua cota, isso não faz com que os estados com menos habitantes paguem menos por seus representantes.
# 
# Estados com grande volume de habitantes, como SP e MG, o custo per capita de um parlamentar é menor. Logo, o custo do parlamentar é inversamente proporcional ao número de habitantes. 

# Aqui concluimos a análise com base nas questões elaboradas pela 99.
# 
# **Vamos tentar responder mais algumas questões !**
# 

# ## Questões adicionais
# 
# **Qual a empresa de telefonia que mais arrecada com as cotas parlamentares ?** 
# 
# **E qual a empresa de viagens aéreas ?**
# 
# **Qual parlamentar estado de SP gastou mais com combustível em 2016 ?**
# 
# **Qual o dia da semana com a maior média de gastos ?**
# 
# **Qual região serviços postais ?**
# 
# **Qual é o parlamentar que usa mais serviços postais ?**
# 

# **Qual empresa de telefonia que mais arrecadou com as cotas parlamentares ?**
# 
# 

# In[108]:


df_mandato_geral.head()


# In[109]:


df_telefonia = df_mandato_geral[df_mandato_geral['txtDescricao']=='TELEFONIA']

df_telefonia.groupby('txtFornecedor')['vlrLiquido'].sum().sort_values(ascending=False).head(20).plot(kind='bar', title =' Principais fornecedores de telefonia',
                                                                                                    figsize = (15,8));


# Os maiores gastos estão relacionados ao celular funcional, que deve ser o celular fornecido pelo próprio Senado. Ramal, também deve estar relacionado a gastos no próprio escritório.
# 
# As gigantes como TIM e Vivo aparecem a partir da quarta posição, seguidas pela conta de telefona do imóvel funcional. 

# **E qual empresas de viagens aéreas ?**

# In[110]:


df_aerea = df_mandato_geral[df_mandato_geral['txtDescricao']=='PASSAGENS AÉREAS']

passagem = df_aerea.groupby('txtFornecedor')['vlrLiquido'].mean().sort_values(ascending=False).head(20).plot(kind='bar', title =' Principais fornecedores de passagens aéres',
                                                                                                    figsize = (15,8));


# Muitas empresas desconhecidas do grande público, provavelmente operam em pequenos trajetos. São denominadas taxis aéreos.

# **Qual parlamentar do estado de SP gastou mais com combustível em 2016 ?**

# In[111]:


df_2016_SP = df_mandato_geral[(df_mandato_geral['numAno']==2016) & (df_mandato_geral['sgUF'] == 'SP')]


# In[112]:


df_2016_SP_comb = df_2016_SP[df_2016_SP['txtDescricao'] == 'COMBUSTÍVEIS E LUBRIFICANTES.']


# In[113]:


df_2016_SP_comb.groupby('txNomeParlamentar')['vlrLiquido'].sum().sort_values(ascending=False).head(5)


# Estes são os cinco parlamentares de SP que mais gastaram com combustíveis em 2016. Vanderlei Macris, é o segundo parlamentar que mais gastou no mandato de 2011 a 2014 lembram ?

# **Qual o dia da semana com a maior média de gastos ?**

# In[114]:


df_mandato_geral.groupby('dia_semana')['vlrLiquido'].mean().plot(kind='bar', title="Gasto médio por dia da semana",
                                                                figsize=(15,8));


# Segunda tem o valor mais elevado de gasto médio. A diferença entre os dias é baixa, o que chama atenção, uma vez que os parlamentares trabalham apenas tres dias na semana. 

# **Qual região mais gasta com serviços postais ?**

# In[115]:


df_postagens = df_mandato_geral[df_mandato_geral['txtDescricao'] == 'SERVIÇOS POSTAIS']


# In[116]:


df_postagens.groupby('REGIAO')['vlrLiquido'].sum().round().sort_values(ascending=False)


# Sudeste, a região mais desenvolvida do país é a líder dos gastos com postagens. Quem é o maior fornecedor ?

# In[117]:


df_postagens.groupby(['txtDescricao', 'txtFornecedor'])['vlrLiquido'].sum().round().sort_values(ascending=False).head()


# Estes são os serviços postais mais utilizados. Pelo menos, o valor é gasto com os correios, que é uma empresa estatal.

# **Qual é o parlamentar que usa mais serviços postais ?**

# In[118]:


df_postagens.groupby(['txtDescricao', 'txNomeParlamentar', 'sgUF', 'txtFornecedor', 'sgPartido'])['vlrLiquido'].sum().round().sort_values(ascending=False).head()


# Renzo Braz de Minas Gerais do PP é disparado, o parlamentar que mais envia correspondências via Sedex. O que serão que ele tanto envia. 
# 
# Acho que essa resposta não estará neste dataset.

# ## Conclusão

# Após analisar o conjunto de dados das cotas parlamentares desde 2009, essas são as principais conclusões:
#     
# * Independentemente da situação do país, os gastos das cotas sempre cresceram;
# 
# * Os gastos com cotas, praticamente dobraram entre 2009 e 2017;
# 
# * Os parlamentares os maiores custos são de passagens aéreas, combustíveis e telefonia;
# 
# * O parlamentar com maior volume de gastos entre 2011 e 2014 é Henrique Fontana do PT;
# 
# * O parlamentar com menor volume de gastos entre 2011 e 2014 é Eunício Oliveira;
# 
# * Os paralamentares de SP, MG e RS são os que mais gastam com cota parlamentar, não a toa o sr Henrique Fontana vem de RS;
# 
# * Curiosamente, gastos com correios estão em 3 lugar na lista de categorias mais onerosas;
# 
# * Os cidadão que pagam mais caro por seus representantes são: Amapa, Acre e Roraima. Isso acontece pois suas cotas paralamentares estão entre as mais altas do Brasil (por volta de 45.000 por político). Entre 2009 e 2018 os 800 mil habitantes do Acre precisam desembolsar em média 26 reais para arcar com os gastos de seus representantes. Isso é um pouco contraditório, pois estados onde o gasto é muito maior, como SP e MG, os habitantes desembolsam em média menos de 5 reais. Isso ocorre por que SP tem mais de 45 milhões de habitantes. Essa iformação foi realmente surpreendente para mim.
# 
# Durante a minha análise confesso que fiquei surpreso e não fazia ideia do valor que o contribuinte paga todo o mes para os parlamentares do nosso país. Este valor exorbitante ainda é completado por um salário de mais de 30 mil reais, auxílio moradia e verba de gabinete de quase 100 mil reais. Isso sem contar que trabalham apenas 3 dias por semana e entre agosto e dezembro eles não trabalham (mas continuam gastando com a verba parlamentar). 
# 
# Por estes e outros motivos é que podemos explicar o motivo da política no nosso país ter se tornado uma carreira e não a oportunidade de representar o mais necessitados e defender os interesses do povo. 
# 
# Como vimos, entre os parlamentares que mais gastaram o nosso dinheiro figuram políticos corruptos e dentre os que menos gastaram, temos condenados pela justiça. 
# 
# Enquanto isso, o país ainda sofre tentando se recuperar de sua maior recessão, o salário mínimo não atingiu sequer mil reais e o desemprego atinge milhões de brasileiros honestos. 
# 
# 

# ### Limitações
# 
# É válido e muito importante comentar que as análises aqui realizadas podem ter sofrido algum tipo de impacto decorrente de algumas limitações que o conjunto de dados impos, e por conta de tais limitações algumas alterações foram necessárias.
# 
# Seguem tais alterações:
# 
# nuLegislatura: Temos apenas 7 valores nulos, irei excluir essas linhas, acredito que esse número não irá prejudicar a análise.
# 
# Exclusão de 3786 valores nulos, nas colunas 'sgUF' e 'sgPartido'
# 
# 
# Transformação de alguns dados incosistentes na coluna datEmissao, esses valores foram excluidos do dataset e representaram cerca de 1,4% do volume total de observações;
# 
# Também não estamos livres de coleta de dados indenvidas ou valores errados. Contudo, espero que essa análise possa ter trazido alguma informação até o momento desconhecida para o leitor.
# 
# 
# Muito obrigado pela atenção.
# 
# 
# 
# **Bruno Batista - 20/11/2018**
