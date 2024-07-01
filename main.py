import pandas as pd
import classificador
import streamlit as st

st.set_page_config(layout='wide')

st.title("Previsão de Inadimplência")

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Carregando modelo"):
        modelo = classificador.carrega_modelo("modelos/modelo_final")
        ohe = classificador.carrega_modelo("modelos/ohe")
        return modelo, ohe

modelo, ohe = load_data()

col1, col2, col3 = st.columns(3)

# ['idade_da_pessoa', 'renda_da_pessoa',
#        'propriedade_da_residencia_da_pessoa', 'tempo_de_emprego_da_pessoa',
#        'intencao_do_emprestimo', 'grau_do_emprestimo', 'valor_do_emprestimo',
#        'taxa_de_juros_do_emprestimo', 'status_do_emprestimo',
#        'percentual_da_renda_comprometido_pelo_emprestimo',
#        'registro_de_inadimplencia_da_pessoa',
#        'tempo_de_histórico_de_credito_da_pessoa']

with col1:
    idade_da_pessoa = st.number_input('Idade da Pessoa', min_value=0, max_value=100)
    renda_da_pessoa = st.number_input('Renda da Pessoa', min_value=1)
    propriedade_da_residencia_da_pessoa = st.selectbox('Propriedade da Residência', ("Hipoteca", "Aluguel", "Próprio", "Outro"))
    tempo_de_emprego_da_pessoa = st.number_input('Tempo de emprego da pessoa', min_value=0, max_value=100)
    intencao_do_emprestimo = st.selectbox('Intenção', ("Consolidação de Dívidas", "Despesas Médicas",
                                                       "Educação", "Empreendimento", "Reforma Residencial",
                                                       "Despesas Pessoais"))
with col2:
    grau_do_emprestimo = st.selectbox('Grau do Empréstimo', ("A", "B", "C", "D", "E", "F", "G"))
    valor_do_emprestimo = st.number_input('Valor do empréstimo', min_value=0)
    taxa_de_juros_do_emprestimo = st.number_input('Taxa de juros do emprestimo', min_value=0.0, step=0.01)
    registro_de_inadimplencia_da_pessoa = st.selectbox('Registro de inadimp.', ('Sim', 'Não'), )
    tempo_de_histórico_de_credito_da_pessoa = st.number_input('Tempo hist. credito', min_value=0, max_value=100)

with col3:
    if st.button("Classificar Cliente"):
        dados = pd.DataFrame([[idade_da_pessoa, renda_da_pessoa, propriedade_da_residencia_da_pessoa, tempo_de_emprego_da_pessoa,
                              intencao_do_emprestimo, grau_do_emprestimo, valor_do_emprestimo, taxa_de_juros_do_emprestimo,
                              registro_de_inadimplencia_da_pessoa, tempo_de_histórico_de_credito_da_pessoa]],
                             columns=['idade_da_pessoa', 'renda_da_pessoa', 'propriedade_da_residencia_da_pessoa',
                                      'tempo_de_emprego_da_pessoa', 'intencao_do_emprestimo', 'grau_do_emprestimo',
                                      'valor_do_emprestimo', 'taxa_de_juros_do_emprestimo',
                                        'registro_de_inadimplencia_da_pessoa', 'tempo_de_histórico_de_credito_da_pessoa'])

        resultado = classificador.classificar_cliente(dados, modelo, ohe)
        if resultado[0] == 0:
            st.markdown("Cliente **NÃO-Inadimplente**")
        else:
            st.markdown("Cliente **INADIMPLENTE**")

