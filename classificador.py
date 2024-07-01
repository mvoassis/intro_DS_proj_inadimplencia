import pandas as pd
import pickle


def carrega_modelo(nome_arquivo):
    nome_arquivo = nome_arquivo + '.pkl'
    with open(nome_arquivo, 'rb') as arquivo:
        modelo = pickle.load(arquivo)
    print(f"Modelo carregado de {nome_arquivo}")
    return modelo


def organiza_dados(dados, ohe):
    dados = dados.copy()

    # encoding on_off
    if dados['registro_de_inadimplencia_da_pessoa'].values == 'Sim':
        dados['registro_de_inadimplencia_da_pessoa'] = 1
    else:
        dados['registro_de_inadimplencia_da_pessoa'] = 0

    # One-Hot Encoder
    novos_dados = pd.DataFrame(ohe.transform(dados.select_dtypes('object')),
                columns=ohe.get_feature_names_out(), index=dados.index)

    for coluna in novos_dados.columns:
        dados[coluna] = novos_dados[coluna]

    dados = dados.drop(['propriedade_da_residencia_da_pessoa', 'intencao_do_emprestimo', 'grau_do_emprestimo'], axis=1)

    # Criando a var. Endividamento
    dados['endividamento'] = (dados['valor_do_emprestimo']*dados['taxa_de_juros_do_emprestimo'])/dados['renda_da_pessoa']

    return dados


def classificar_cliente(dados, modelo_final, ohe):
    dados = organiza_dados(dados, ohe)
    y_pred = modelo_final.predict(dados)
    return y_pred