import json
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def getData(languages, base='dirty'):
    fonemasALL = []
    fonemasLABELS = languages#['cs', 'en', 'de']
    cores = ['green', 'blue', 'yellow', 'red', 'purple', 'crimson']  # Adicione mais mapeamentos conforme necessário
    mapeamento_cores = {}  # Adicione mais mapeamentos conforme necessário
    for i in range(len(fonemasLABELS)):
        mapeamento_cores[fonemasLABELS[i]] = cores[i]

    for lang_code in fonemasLABELS:
        with open('word_data/{}/{}.json'.format(base, lang_code), 'r') as file:
            dados = file.read()
        fonemasALL.append(json.loads(dados))


    fonemaList = []
    for fonemas in fonemasALL:
        for word in fonemas:
            for f in fonemas[word]:
                if f not in fonemaList and f != ' ':
                    fonemaList.append(f)

    # print(fonemaList)

    dataframe = {'word': [], 'phoneme': [], 'language': []}
    for f in fonemaList:
        dataframe[f] = []

    for i in range(len(fonemasALL)):
        fonemas = fonemasALL[i]
        for word in fonemas:
            dataframe['word'].append(word)
            dataframe['phoneme'].append(fonemas[word])
            dataframe['language'].append(fonemasLABELS[i])
            for f in fonemaList:
                dataframe[f].append(fonemas[word].count(f))

    df = pd.DataFrame(data=dataframe)
    # print(df)


    # Supondo que você já possui um DataFrame chamado 'dados' com as suas colunas e dados,
    # e as duas primeiras colunas são as colunas de identificação

    # Armazenar as duas primeiras colunas em uma nova variável
    colunas_identificacao = df.iloc[:, 0:3]

    # Excluir as duas primeiras colunas e a terceira coluna (categoria) do DataFrame original
    dados = df.iloc[:, 3:]

    # Criar uma instância do objeto PCA
    pca = PCA(n_components=2)  # Defina o número de componentes desejado (2 para visualização em um gráfico)

    # Aplicar o PCA aos seus dados
    dados_reduzidos = pca.fit_transform(dados)

    # Converter os dados reduzidos em um novo DataFrame
    dados_reduzidos = pd.DataFrame(dados_reduzidos, columns=['Componente 1', 'Componente 2'])

    # Concatenar as colunas de identificação com os dados reduzidos
    dados_reduzidos = pd.concat([colunas_identificacao, dados_reduzidos], axis=1)

    legendas = []
    for categoria in dados_reduzidos['language'].unique():
        legendas.append(plt.scatter([], [], c=mapeamento_cores[categoria], label=categoria))

    # print({'data': dados_reduzidos, 'labels': fonemasLABELS, 'colors': cores})
    return {'data': dados_reduzidos, 'labels': fonemasLABELS, 'colors': cores}

    # Obter as cores correspondentes a cada categoria
    # cores = [mapeamento_cores[categoria] for categoria in colunas_identificacao['language']]

    # Plotar os pontos em um gráfico de dispersão, com cores diferentes para cada categoria
    # plt.scatter(dados_reduzidos['Componente 1'], dados_reduzidos['Componente 2'], c=cores)
    # plt.xlabel('Componente 1')
    # plt.ylabel('Componente 2')
    # plt.title('Redução de dimensionalidade usando PCA')
    # plt.legend(handles=legendas)
    # plt.show()
