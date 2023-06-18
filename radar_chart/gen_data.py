import json
from collections import Counter
import sys

def getData(languages, base='dirty'):
        # Obtém o nome do arquivo a partir do argumento
    fonemasALL = []
    fonemasLABELS = languages
    # Abre o arquivo JSON
    for lang_code in fonemasLABELS:
        with open('word_data/{}/{}.json'.format(base, lang_code), 'r') as file:
            dados = file.read()
        fonemasALL.append(json.loads(dados))

    # Cria um único string com todos os fonemas
    data = []
    for lang in fonemasALL:
        fonemas = ''.join(lang.values())

        # Conta a ocorrência de cada fonema
        contador_fonemas = Counter(fonemas)

        # Converte o resultado em um array de tuplas (fonema, quantidade)
        resultado = [(fonema, quantidade) for fonema, quantidade in contador_fonemas.items()]
        resultado_ordenado = sorted(resultado, key=lambda x: x[1], reverse=True)
        # Exibe o resultado

        # Cria um novo dicionário apenas com os primeiros registros
        dicionario_registros = {fonema: quantidade for fonema, quantidade in resultado_ordenado}
        data.append(dicionario_registros)
    
    #Verificar o fonema mais frequente em cada língua e verificar a frequencia do mesmo fonema nas outras línguas contidas em data
    fonemas_mais_frequentes = []
    for lang in data:
        fonemas_mais_frequentes.append(list(lang.keys())[0])
    dados_finais = []

    for fonema in fonemas_mais_frequentes:
        ocorrencias = [lang.get(fonema, 0) for lang in data]
        dados_finais.append([fonema] + ocorrencias)


    data = dados_finais


    # Define o nome do arquivo de saída
    cores = ['green', 'blue', 'yellow', 'red', 'purple', 'crimson']
    return {'data': data, 'labels': fonemasLABELS, 'colors': cores}
