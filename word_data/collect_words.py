import requests
from numpy import inf

from phonemizer import phonemize
from phonemizer.separator import Separator

import json

from sys import argv

phonemizer_version = {
   'en':'en-us',
   'fr': 'fr-fr',
   'pt': 'pt-br',
   'zh': 'cmn',
   'cs':'cs',
   'de':'de',
   'es':'es',
   'fa':'fa',
   'hi':'hi',
   'hu':'hu',
   'it':'it',
   'ru':'ru',
   'sv':'sv',
   'tr':'tr'
}

def obter_palavras_dirtywords(lingua):
  response = requests.get('https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/{}'.format(lingua))
  palavras = str(response.content,"utf-8")
  return palavras.split('\n')

def obter_palavras_wiktionary(url_api, max_calls = inf):
    palavras = set()
    continuar = True
    cont_continue = 0
    start_title = '!'
    step = 500  # Número de palavras a serem obtidas em cada consulta
    
    while continuar:
        params = {
            'action': 'query',
            'list': 'allpages',
            'aplimit': step,
            'apfilterredir': 'nonredirects',
            'format': 'json',
            'apfrom': start_title
        }

        response = requests.get(url_api, params=params)
        data = response.json()

        for page in data['query']['allpages']:
            palavra = page['title']
            palavras.add(palavra)
        
        cont_continue += 1

        if 'continue' in data and cont_continue < max_calls:
            start_title = data['continue']['apcontinue']
        else:
            continuar = False
        
        print(f"Língua: {url_api[8:10]}, Consultas realizadas: {cont_continue}, Palavras obtidas: {len(palavras)}")
    
    return sorted(list(palavras))

def filtrar_palavras_validas(palavras):
  palavras_filtradas = []

  for palavra in palavras:
    palavra = palavra.strip()
    if palavra != '' and palavra[0].isalpha() and palavra[-1].isalpha():
      palavras_filtradas.append(palavra)
  
  return palavras_filtradas


def obter_fonemas(palavras, lingua='pt-br'):
  phos = phonemize(palavras,
    language=lingua,
    backend="espeak",
    separator=Separator(phone=None, word=' ', syllable='|'),
    strip=True,
    preserve_punctuation=True,
    njobs=4)

  return [str(pho) for pho in phos]


_, lang_code, base = argv

palavras = []

if base == 'dirty':
  palavras = obter_palavras_dirtywords(lang_code)

elif base == 'clean':
  url_api = "https://{}.wiktionary.org/w/api.php".format(lang_code)
  palavras = obter_palavras_wiktionary(url_api)

else:
   exit()

palavras = filtrar_palavras_validas(palavras)

fonemas = obter_fonemas(palavras, phonemizer_version[lang_code])

data = dict(zip(palavras, fonemas))

with open('{}/{}.json'.format(base,lang_code),'w') as f:
  f.write(json.dumps(data, indent=4, sort_keys=True))
