import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Criando o aplicativo Dash
app = dash.Dash(__name__)

# Carregando dados de exemplo
df = None
try:
    df = pd.read_csv('venv/dados.csv')  # Verifique se o caminho para o arquivo está correto
    print("Dados lidos com sucesso:")
    print(df)
except FileNotFoundError:
    print("Erro: Arquivo 'dados.csv' não encontrado.")
except pd.errors.EmptyDataError:
    print("Erro: Arquivo 'dados.csv' está vazio.")
except Exception as e:
    print(f"Erro ao ler o arquivo CSV: {e}")

# Somente prossiga se o DataFrame foi lido corretamente
if df is not None:
    # Cálculo do IMC
    df['Imc'] = df['Weight'] / (df['Height'] * df['Height'])

    # Filtrando dados para obesidade e abaixo do peso
    df_obesidade = df[df['Imc'] > 30]
    df_abaixo_peso = df[df['Imc'] < 18.5]

    # Adicionando colunas de histórico familiar e IMC
    df['Historico Familiar E Obeso'] = (df['family_history_with_overweight'] == 'yes') & (df['Imc'] > 30)
    df['Historico Familiar E Abaixo do peso'] = (df['family_history_with_overweight'] == 'yes') & (df['Imc'] < 18.5)

    colunas = ['family_history_with_overweight', "Imc", "Historico Familiar E Obeso", 'Historico Familiar E Abaixo do peso']
    historicoFamiliarImc = df[colunas]

    # Criar gráfico de violino para IMC por idade com distribuição normal
    violino_imc_por_idade = px.violin(df, y='Imc', x='Age', title='Distribuição do IMC por Faixa Etária',
                                      labels={'Age': 'Idade', 'Imc': 'IMC'},
                                      box=True, points="all", hover_data=df.columns)
    # Adicionar distribuição normal ao gráfico de violino
    for age in df['Age'].unique():
        age_group = df[df['Age'] == age]['Imc']
        mean = age_group.mean()
        std = age_group.std()
        x = np.linspace(mean - 3*std, mean + 3*std, 100)
        y = (1 / (np.sqrt(2 * np.pi) * std)) * np.exp(-0.5 * ((x - mean) / std) ** 2)
        violino_imc_por_idade.add_trace(go.Scatter(x=[age]*len(x), y=x, mode='lines', name=f'Normal Distribution (Age {age})'))

    # Criar histograma para a distribuição de idades
    histograma_idade = px.histogram(df, x='Age', nbins=5, title='Distribuição de Idade dos Participantes')

    # Gráfico de dispersão para idade vs IMC (abaixo do peso)
    scatter_abaixo_peso = px.scatter(df_abaixo_peso, x="Age", y="Imc", title='Idade vs IMC (Abaixo do Peso)',
                                     labels={'Age': 'Idade', 'Imc': 'IMC'})

    # Gráfico de barras empilhadas para histórico familiar de obesidade vs IMC
    df['Obesidade'] = df['Imc'] > 30
    barras_historico_familiar_obesidade = px.histogram(df, x='family_history_with_overweight', y='Imc', color='Obesidade',
                                                       barmode='stack', title='Histórico Familiar de Obesidade vs IMC',
                                                       labels={'family_history_with_overweight': 'Histórico Familiar de Obesidade', 'Imc': 'IMC'})

    # Calculando a porcentagem de fumantes que consomem álcool
    porcentagemFumantesAlcoolTodos = (df[(df['SMOKE'] == 'yes') & (df['CALC'] != 'no')].shape[0] / df[df['SMOKE'] == 'yes'].shape[0]) * 100

    # Calculando o número de jovens abaixo do peso com pais obesos
    PaisObesosJovemAbaixoDoPeso = df[((df['family_history_with_overweight'] == 'yes') & (df['Imc'] < 18.5))].shape[0]

    # Calculando a probabilidade de encontrar um jovem obeso com pais obesos
    total_jovens = df.shape[0]
    jovens_obesos_pais_obesos = df[(df['Imc'] > 30) & (df['family_history_with_overweight'] == 'yes')].shape[0]
    prob_jovem_obeso_pais_obesos = (jovens_obesos_pais_obesos / total_jovens) * 100

    # Calculando a probabilidade de encontrar um jovem abaixo do peso com pais obesos
    jovens_abaixo_peso_pais_obesos = df[(df['Imc'] < 18.5) & (df['family_history_with_overweight'] == 'yes')].shape[0]
    prob_jovem_abaixo_peso_pais_obesos = (jovens_abaixo_peso_pais_obesos / total_jovens) * 100

    # Layout da aplicação
    app.layout = html.Div(children=[
        html.H1(children='Análise de Dados de Saúde'),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H2(children='Distribuição da Idade dos Participantes'),
                        html.P("Boxplot mostrando a distribuição das idades dos participantes, destacando os quartis e possíveis outliers."),
                        dcc.Graph(
                            id='box-plot-1',
                            figure=px.box(df, y='Age', title='Distribuição da Idade dos Participantes')
                        ),
                    ],
                    style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}
                ),
                html.Div(
                    children=[
                        html.H2(children='Distribuição do IMC por Faixa Etária'),
                        html.P("Gráfico de violino mostrando a distribuição do IMC em diferentes faixas etárias com uma curva de distribuição normal."),

                        dcc.Graph(
                            id='grafico-violino-imc-idade',
                            figure=violino_imc_por_idade
                        ),
                    ],
                    style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}
                ),
            ],
        ),
        html.Div(
            children=[
                html.H2(children='Distribuição da Idade dos Participantes'),
                html.P("Histograma mostrando a distribuição das idades dos participantes."),
                dcc.Graph(
                    id='histograma-idade',
                    figure=histograma_idade
                ),
            ],
            style={'margin-top': '20px', 'padding': '20px'}
        ),
        html.Div(
            children=[
                html.H2(children='Idade vs IMC (Abaixo do Peso)'),
                html.P("Gráfico de dispersão mostrando a relação entre idade e IMC para pessoas abaixo do peso."),
                html.P(
                    "Percebe-se que as pessoas com IMC mais baixo se concentram entre 23 e 17 anos de idade"),

                dcc.Graph(
                    id='grafico-abaixo-peso',
                    figure=scatter_abaixo_peso
                ),
            ],
            style={'margin-top': '20px', 'padding': '20px'}
        ),
        html.Div(
            children=[
                html.H2(children='Histórico Familiar de Obesidade vs IMC'),
                html.P(
                    "Gráfico de barras empilhadas mostrando a relação entre histórico familiar de obesidade e a distribuição de IMC."),
                html.P(
                    "Este gráfico ilustra a relação entre o histórico familiar de obesidade e o índice de massa corporal (IMC). Observa-se uma forte correlação entre o histórico familiar e o IMC dos jovens, indicando uma possível influência dos hábitos alimentares dos pais sobre o IMC de seus filhos."),

                dcc.Graph(
                    id='grafico-historico-familiar-obesidade',
                    figure=barras_historico_familiar_obesidade
                ),
            ],
            style={'margin-top': '20px', 'padding': '20px'}
        ),
        html.Div(
            children=[
                html.H2(children='Porcentagem de Fumantes que Consomem Álcool'),
                html.P(f"{porcentagemFumantesAlcoolTodos:.2f}% dos fumantes consomem álcool"),
                html.P("Esta métrica indica a porcentagem de participantes que são fumantes e também consomem álcool, oferecendo uma visão sobre a coocorrência desses dois comportamentos.")
            ],
            style={'margin-top': '20px', 'padding': '20px'}
        ),
        html.Div(
            children=[
                html.H2(children='Número de Jovens Abaixo do Peso com Pais Obesos'),
                html.P(f"{PaisObesosJovemAbaixoDoPeso} jovens têm histórico familiar de obesidade e estão abaixo do peso."),
                html.P("Esta métrica fornece uma visão sobre quantos jovens têm pais com histórico de obesidade e, ao mesmo tempo, estão abaixo do peso.")
            ],
            style={'margin-top': '20px', 'padding': '20px'}
        ),
        html.Div(
            children=[
                html.H2(children='Probabilidade de Jovem Obeso com Pais Obesos'),
                html.P(f"A probabilidade de um jovem ser obeso, dado que seus pais são obesos, é de {prob_jovem_obeso_pais_obesos:.2f}%."),
                html.P("Essa métrica fornece uma estimativa da probabilidade de um jovem ser obeso, sabendo que seus pais são obesos.")
            ],
            style={'margin-top': '20px', 'padding': '20px'}
        ),
        html.Div(
            children=[
                html.H2(children='Probabilidade de Jovem Abaixo do Peso com Pais Obesos'),
                html.P(f"A probabilidade de um jovem estar abaixo do peso, dado que seus pais são obesos, é de {prob_jovem_abaixo_peso_pais_obesos:.2f}%."),
                html.P("Essa métrica fornece uma estimativa da probabilidade de um jovem estar abaixo do peso, sabendo que seus pais são obesos.")
            ],
            style={'margin-top': '20px', 'padding': '20px'}
        )
    ])

    # Executando o servidor
    if __name__ == '__main__':
        app.run_server(debug=True)
else:
    print("Não é possível configurar o layout da aplicação, pois o DataFrame não foi carregado.")
