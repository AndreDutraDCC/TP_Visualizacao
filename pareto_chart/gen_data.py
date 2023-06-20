import json
import pandas as pd

def getData(languages, base='dirty', by_family=False):
    fonemasALL = []
    fonemasLABELS = languages
    
    with open('word_data/language_info.json', 'r') as file:
        languageData = json.loads(file.read())

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

    dataframe = {'language_key': [], 'language': [], 'family': [], 'total': []}

    for f in fonemaList:
        dataframe[f] = []

    for i in range(len(fonemasALL)):
        dataframe['language_key'].append(fonemasLABELS[i])
        dataframe['language'].append(languageData[fonemasLABELS[i]][0])
        dataframe['family'].append(languageData[fonemasLABELS[i]][1])
        words = fonemasALL[i]
        total = 0
        for f in fonemaList:
            dataframe[f].append(0)
        for word in words:
            for f in fonemaList:
                n = word.count(f)
                total += n
                dataframe[f][i] += n
        dataframe['total'].append(total)


    df = pd.DataFrame(data=dataframe)

    return {'data': df, 'languages': fonemasLABELS, 'fonemas': fonemaList, 'languageData': languageData} # frequency = {'language: {'fonema': [amount, percent]}}

