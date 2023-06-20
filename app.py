import os
import pandas as pd
from flask import Flask, render_template

import scatter_chart.gen_data as scatter_data
import radar_chart.gen_data   as   radar_data
import network_chart.gen_data as network_data

import json
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.io import to_json

from seaborn import color_palette



app = Flask(__name__)

@app.route('/')
def index():
    routes = [
        {'link': "primeira", 'title': "Scatter", 'key': 0, 'isChart':True},
        {'link': 'segunda', 'title': "Radar", 'key': 1, 'isChart':False},
        {'link': "terceira", 'title': "Bubble", 'key': 2, 'isChart':False}
    ] # Page Names

    # Get visualizations info
    chartInfo = [getChartInfo1(), getChartInfo2(), getChartInfo3()]

    props = {'routes': routes, 'chartInfo':chartInfo}

    return render_template('index.html', props=props)


def getLanguages(base="dirty"):
    langs = []
    dir = "word_data/" + base

    for d in os.listdir(dir):
        langs.append(d[:-5])
    
    ordered_langs = ['es','pt','fr','it','de','en','ru','sv','tr','hu','cs','hi','zh','fa']

    return [lang for lang in ordered_langs if lang in langs]

def getColorMap(alpha=1):
    all_languages = ['es','pt','fr','it','de','en','ru','sv','tr','hu','cs','hi','zh','fa']
    all_colors = ['rgba({},{},{},{})'.format(*(round(255*val) for val in color), alpha) for color in color_palette('husl',14)]
    return dict(zip(all_languages, all_colors))

def getLanguageInfo():
    with open('word_data/language_info.json', 'r') as f:
        return json.load(f)

def getChartInfo1():
    colormap = getColorMap(0.6)

    data1 = scatter_data.getData(getLanguages())
    datasets = []
    # print(data1)
    for l_key in data1["labels"]:
        datasets.append({
            'label': data1["languageData"][l_key][0],
            'data' : [{'x': row["Componente 1"], 'y': row["Componente 2"], 'word': row["word"]} for index, row in data1['data'].iterrows() if row['language'] == data1["languageData"][l_key][0]],
            'backgroundColor': colormap[l_key]
        })
    data = {
    'datasets': datasets,
    }
    config = {
        'type': 'scatter',
        'data': data,
        'options': {
            'plugins': {
                'zoom': {
                    'pan': {
                        'enabled': True,
                        'mode': 'xy',
                    },
                    'zoom': {
                        'wheel': {
                            'enabled': True
                        },
                        'pinch': {
                            'enabled': True
                        },
                        'mode': 'xy',
                    },
                }
            },
            'scales': {
                'x': {
                    'type': 'linear',
                    'position': 'bottom'
                }
            }
        }
    }

    return config

def getChartInfo2():
    languages = getLanguages()
    lang_info = getLanguageInfo()
    colormap = getColorMap(0.8)

    data, phonems, _ = radar_data.getData(languages,'dirty').values()
    
    rows = 4
    columns = 4
    
    fig = make_subplots(rows, columns, specs=[[{'type': 'polar'}]*columns]*rows, subplot_titles=[lang_info[lang][0] for lang in languages])

    plots = []

    for language in languages:
        plots.append(go.Scatterpolar(theta = phonems,
                                     r = data.loc[language,'vector'],
                                     mode = 'lines',
                                     fill = 'toself',
                                     marker={'color':colormap[language]},
                                     showlegend=False))
    
    k = 0
    for i in range(1, rows+1):
        for j in range(1, columns+1):
            fig.add_trace(plots[k], i, j)
            k+=1
            if k == 14: break
        if k == 14: break
    
    fig.update_layout(title = 'Meu título', xaxis={'title':'aaaaaa'})

    for k, language in enumerate(languages):
        fig.update_layout({'polar{}'.format(k+1 if k!=0 else ''): {
            'radialaxis': {
                'showticklabels': False
            },
            'angularaxis': {
                'tickfont': {'size':8}
            }}})
        test = fig['layout']['polar']['radialaxis']['range']
        new_pos = fig['layout']['annotations'][k]['y'] - 0.22
        fig.update_annotations(y=new_pos, selector={'text':lang_info[language][0]})

    info = json.loads(to_json(fig))
    return info

def getChartInfo3():
    languages = getLanguages('dirty')
    colormap = getColorMap()

    response = network_data.getData(languages, 'dirty', 5)

    nodes_df, edges_data, labels = response.values()

    plots = []

    for x, y in edges_data.values():
        plots.append(dict(x=x,
                          y=y,
                          type='scatter',
                          mode='lines',
                          marker={'color':'rgb(200,200,200)'},
                          showlegend=False))

    lang_info = getLanguageInfo()
    
    for lang in labels:
        row = nodes_df.loc[lang]

        plots.append(go.Scatter(x=[row['x']],
                                y=[row['y']],
                                mode='markers',
                                marker={'color':colormap[lang],
                                        'size': 25},
                                hovertemplate='%{text}',
                                text=['language: <b>{}</b><br>family: <b>{}</b>'.format(*lang_info[lang])],
                                hoverlabel={'align':'right'},
                                showlegend=False
                                ))
    fig = go.Figure(data= plots, 
                    layout = go.Layout(title='Grafo de línguas ligadas por proximidade fonética',
                                       xaxis={'visible':False},
                                       yaxis={'scaleanchor':'x', 'scaleratio':1, 'visible':False},
                                       plot_bgcolor='white',
                                       hovermode='closest',
                                       hoverlabel={'font':{'color':'white'}}))
    
    for lang, row in nodes_df.iterrows():
        fig.add_annotation(x=row['x'],
                           y=row['y'],
                           text='<b>{}</b>'.format(lang),
                           showarrow=False,
                           font={'color':'rgb(255,255,255)'})
    
    info = json.loads(to_json(fig))

    return info

if __name__ == '__main__':
    app.run(debug=True)
