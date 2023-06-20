import os
import pandas as pd
from flask import Flask, render_template

import scatter_chart.gen_data as scatter_data
# import radar_chart.gen_data   as   radar_data
# import network_chart.gen_data as network_data


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
    return langs

def getChartInfo1():
    data1 = scatter_data.getData(getLanguages())
    datasets = []
    # print(data1)
    for l_key in data1["labels"]:
        datasets.append({
            'label': data1["languageData"][l_key][0],
            'data' : [{'x': row["Componente 1"], 'y': row["Componente 2"], 'word': row["word"]} for index, row in data1['data'].iterrows() if row['language'] == data1["languageData"][l_key][0]],
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
    info = {
        'data': [
            {
                'x': [1, 2, 3, 4, 5],
                'y': [1, 4, 9, 16, 25],
                'type': 'scatter',
            }
        ],
        'layout': {
            'title': 'Plotly Graph 1',
        }
    }
    return info

def getChartInfo3():
    info = {
        'data': [
            {
                'x': [3, 4, 5],
                'y': [9, 16, 25],
                'type': 'scatter',
            }
        ],
        'layout': {
            'title': 'Plotly Graph 2',
        }
    }
    return info

if __name__ == '__main__':
    app.run(debug=True)
