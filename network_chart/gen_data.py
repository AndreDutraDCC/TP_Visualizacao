import networkx as nx

import json
import pandas as pd
import numpy as np

from seaborn import color_palette

all_languages = ['es','pt','fr','it','de','en','ru','sv','tr','hu','cs','hi','zh','fa']
all_colors = color_palette('husl',14)
colormap = dict(zip(all_languages, all_colors))

def gen_layout_fruchterman_reingold(dist_matrix):
    graph = nx.from_numpy_array(dist_matrix)
    
    layout_dict = nx.spring_layout(graph,
                                   pos={node: 10*np.random.rand(2) for node in graph.nodes},
                                   fixed=[node for node in graph.nodes if not graph.edges(node)],
                                   k=10,
                                   iterations=60)

    layout_data = [layout_dict[i] for i in range(len(layout_dict))]

    return np.stack(layout_data, axis=1).T

def gen_layout_kamada_kawai(dist_matrix):
    graph = nx.from_numpy_array(dist_matrix)
    
    layout_dict = nx.kamada_kawai_layout(graph)

    layout_data = [layout_dict[i] for i in range(len(layout_dict))]

    return np.stack(layout_data, axis=1).T


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

    n_words = len(df)

    dist_matrix = np.zeros((n_words, n_words))
    edge_data = {}

    for i, u in enumerate(df['vector']):
        for j, v in enumerate(df['vector']):
            dist = np.sum(np.abs(u-v))#np.linalg.norm(u-v)

            if dist < max_dist:
                dist_matrix[i][j] = dist
                edge_data[(i,j)] = []

    print(dist_matrix.mean())
    print(dist_matrix.std())
    
    positions = gen_layout_fruchterman_reingold(dist_matrix)

    x,y = list(zip(*positions))

    df['x'] = x

    df['y'] = y

    for i,j in edge_data:
        edge_data[(i,j)] = [[x[i], x[j]], [y[i], y[j]]]

    
    return {'data': df, 'edge_data': edge_data, 'labels': languages}
