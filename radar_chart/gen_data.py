import numpy as np
import pandas as pd
import json

def vectorize(phonem_word):
    phonems = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'æ', 'ç', 'ð', 'ø', 'ŋ', 'œ', 'ɐ', 'ɑ', 'ɒ', 'ɔ', 'ɕ', 'ɖ', 'ə', 'ɚ', 'ɛ', 'ɜ', 'ɟ', 'ɡ', 'ɣ', 'ɨ', 'ɪ', 'ɫ', 'ɭ', 'ɯ', 'ɲ', 'ɳ', 'ɵ', 'ɹ', 'ɻ', 'ɾ', 'ʀ', 'ʁ', 'ʂ', 'ʃ', 'ʈ', 'ʉ', 'ʊ', 'ʋ', 'ʌ', 'ʎ', 'ʐ', 'ʑ', 'ʒ']
    phonem_counter = {phonem:0 for phonem in phonems}

    for phonem in phonem_word:
        if phonem in phonems:
            phonem_counter[phonem] += 1
    
    return np.array([phonem_counter[phonem] for phonem in phonems])



def getData(languages, base='all', max_dist = np.inf):
    data = {
        'language': [],
        'vector':   []
        }

    direc = base if base != 'all' else 'dirty'
    
    for language in languages:
        with open('word_data/{}/{}.json'.format(direc, language), 'r') as f:
            lang_data = json.load(f)

        for phonem_word in lang_data.values():
            data['language'].append(language)
            data['vector'].append(vectorize(phonem_word))

            if base == 'all':
                with open('word_data/{}/{}.json'.format('clean', language), 'r') as f:
                    lang_data = json.load(f)

                for phonem_word in lang_data.values():
                    data['language'].append(language)
                    data['vector'].append(vectorize(phonem_word))
    
    df = pd.DataFrame(data)
    df = df.groupby('language').mean()
    
    return {'data': df,
            'phonems':['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'æ', 'ç', 'ð', 'ø', 'ŋ', 'œ', 'ɐ', 'ɑ', 'ɒ', 'ɔ', 'ɕ', 'ɖ', 'ə', 'ɚ', 'ɛ', 'ɜ', 'ɟ', 'ɡ', 'ɣ', 'ɨ', 'ɪ', 'ɫ', 'ɭ', 'ɯ', 'ɲ', 'ɳ', 'ɵ', 'ɹ', 'ɻ', 'ɾ', 'ʀ', 'ʁ', 'ʂ', 'ʃ', 'ʈ', 'ʉ', 'ʊ', 'ʋ', 'ʌ', 'ʎ', 'ʐ', 'ʑ', 'ʒ'],
            'labels': languages}