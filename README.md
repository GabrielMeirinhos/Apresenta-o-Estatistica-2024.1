Saude-Data-Analysis-Dashboard
Este projeto é um dashboard interativo desenvolvido com o framework Dash e visualizações do Plotly, focado na análise de dados de saúde. O objetivo é explorar relações entre idade, IMC, histórico familiar e comportamentos de risco como o consumo de álcool e tabaco.

Funcionalidades
Distribuição da Idade dos Participantes: Boxplot e histograma mostrando a distribuição de idades.
Distribuição do IMC por Faixa Etária: Gráfico de violino com curvas de distribuição normal para cada faixa etária.
Idade vs IMC (Abaixo do Peso): Gráfico de dispersão para indivíduos abaixo do peso.
Histórico Familiar de Obesidade vs IMC: Gráfico de barras empilhadas para visualizar a influência do histórico familiar sobre o IMC.
Estatísticas e Probabilidades: Cálculos de porcentagens e probabilidades para características específicas (ex.: fumantes que consomem álcool).
Requisitos
Python 3.7+
Dash
Pandas
Plotly
Instalação
Clone este repositório:

bash
Copiar código
git clone https://github.com/seuusuario/Saude-Data-Analysis-Dashboard.git
cd Saude-Data-Analysis-Dashboard
Instale as dependências:

bash
Copiar código
pip install dash pandas plotly
Certifique-se de que o arquivo dados.csv esteja na pasta venv/. Este arquivo deve conter os dados de saúde dos participantes com as colunas:

Age - Idade dos participantes
Weight - Peso em kg
Height - Altura em metros
family_history_with_overweight - Histórico familiar de obesidade (yes ou no)
SMOKE - Indicação de fumante (yes ou no)
CALC - Consumo de álcool (yes, no, etc.)
Uso
Execute o servidor do Dash:

bash
Copiar código
python app.py
Acesse o dashboard em http://127.0.0.1:8050/.

Estrutura do Código
app.py: Contém o código do dashboard, incluindo carregamento de dados, cálculos e visualizações.
Exemplos de Visualizações
Boxplot: Distribuição de idade dos participantes
Gráfico de Violino: IMC por faixa etária com curva de distribuição normal
Gráfico de Dispersão: Idade vs IMC (abaixo do peso)
Gráfico de Barras Empilhadas: Histórico familiar e IMC
Observações
Caso o arquivo dados.csv não seja encontrado, uma mensagem de erro será exibida.
Este projeto é apenas um exemplo de análise e visualização de dados e não deve ser usado para diagnósticos de saúde.
Contribuição
Sinta-se à vontade para contribuir com melhorias. Faça um fork do projeto e envie um pull request com suas sugestões.

