from fa2 import ForceAtlas2
import json
import pandas as pd
import numpy as np

from seaborn import color_palette

all_languages = ['es','pt','fr','it','de','en','ru','sv','tr','hu','cs','hi','zh','fa']
all_colors = color_palette('husl',14)
colormap = zip(all_languages, all_colors)

forceatlas2 = ForceAtlas2(
                            # Behavior alternatives
                            outboundAttractionDistribution=True,  # Dissuade hubs
                            linLogMode=False,  # NOT IMPLEMENTED
                            adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                            edgeWeightInfluence=1.0,

                            # Performance
                            jitterTolerance=1.0,  # Tolerance
                            barnesHutOptimize=True,
                            barnesHutTheta=1.2,
                            multiThreaded=False,  # NOT IMPLEMENTED

                            # Tuning
                            scalingRatio=2.0,
                            strongGravityMode=False,
                            gravity=1.0,

                            # Log
                            verbose=True)


def vectorize(phonem_word):
    phonems = []
    phonem_counter = {phonem:0 for phonem in phonems}

    for phonem in phonem_word:
        phonem_counter[phonem] += 1
    
    return np.array([phonem_counter[phonem] for phonem in phonems])



def getData(languages, base='dirty', max_dist = np.inf):
    global forceatlas2, colormap

    data = {
        'language':   [],
        'word':       [],
        'phonem_word':[],
        'vector':     [],
        'x':          [],
        'y':          []
        }

    for language in languages:
        lang_data = json.load('/word_data/{}/{}'.format(base, language))

        for word, phonem_word in lang_data.items():
            data['language'].append(language)
            data['word'].append(word)
            data['phonem_word'].append(phonem_word)
            data['vector'].append(vectorize(phonem_word))
            data['x'].append(0)
            data['y'].append(0)
    
    df = pd.DataFrame(data)
    n_words = len(df)

    dist_matrix = np.zeros((n_words, n_words))

    for i, u in enumerate(df['vector']):
        for j, v in enumerate(df['vector']):
            dist_matrix[i][j] = np.linalg.norm(u-v)
    
    positions = forceatlas2.forceatlas2(dist_matrix, np.zeros((n_words,2)), iterations=100)

    for i, (x,y) in enumerate(positions):
        df.iloc['x',i] = x
        df.iloc['y',i] = y
    
    return {'data': df, 'labels': languages, 'colors': [colormap[language] for language in languages]}
