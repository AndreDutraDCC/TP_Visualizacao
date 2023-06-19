from flask import Flask, render_template
import pandas as pd

import scatter_chart.gen_data as scatter_data
import radar_chart.gen_data   as   radar_data
import network_chart.gen_data as network_data

app = Flask(__name__)

@app.route('/')
def index():
    routes = [
        {'link': "primeira", 'title': "Scatter", 'key': 0},
        {'link': 'segunda', 'title': "Radar", 'key': 1},
        {'link': "terceira", 'title': "Bubble", 'key': 2}
    ] # Page Names

    # Get visualizations info
    chartInfo = [getChartInfo1(), getChartInfo2(),getChartInfo3()]

    props = {'routes': routes, 'chartInfo':chartInfo}

    return render_template('index.html', props=props)


def getChartInfo1():
    data1 = scatter_data.getData(['en', 'fr', 'it', 'es', 'pt', 'ru'])
    datasets = []
    for i in range(len(data1["labels"])):
        datasets.append({
            'label': data1['labels'][i],
            'data' : [{'x': row["Componente 1"], 'y': row["Componente 2"], 'word': row["word"]} for index, row in data1['data'].iterrows() if row['language'] == data1['labels'][i]],
        })

    data = {
    'datasets': datasets,
    }
    
    config = {
        'type': 'scatter',
        'data': data,
        'options': {
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
    data1 = radar_data.getData( ['es','pt','fr','it','de','en','ru','sv','tr','hu','cs','hi','zh','fa'])
    datasets = []
    labels = []
    for i in range(len(data1["labels"])):
        labels.append(data1['data'][i][0])
        datasets.append({
            'label': data1['labels'][i],
            'data' : data1['data'][i][1:],
        })

    data = {
        'labels': labels,
        'datasets': datasets,
    }




    config = {
        'type': 'radar',
        'data': data,
        'options': {
            'elements': {
                'line': {
                    'borderWidth': 3
                }
            },
            'scales': {
                'r': {'suggestedMin': 0, 'suggestedMax': 100}
            },
        },
    }

    return config

def getChartInfo3():
    languages = ['es','pt','fr','it','de','en','ru','sv','tr','hu','cs','hi','zh','fa']

    response = network_data.getData(languages, 'dirty', 4.5)

    nodes_df, edges_data, labels, colors = response.values()

    datasets = []

    for lang, color in zip(labels, colors):
        row = nodes_df.loc[lang]

        dataset = {
            'type': 'bubble',
            'label': lang,
            'data': [{
                'x': row['x'],
                'y': row['y'],
                'r': 15
            }],
            'backgroundColor': 'rgb({},{},{})'.format(*(round(255*val) for val in color)),
            'order': 1

        }

        datasets.append(dataset)

    '''for x, y in edges_data.values():
        dataset = {
            'type': 'line',
            'data': y,
            'backgroundColor': 'rgb(200,200,200)',
            'order': 2

        }
        datasets.append(dataset)'''

    
    data = {
        'datasets': datasets
    }
    
    config = {
        'data': data,
        'options': {}
    }

    return config

if __name__ == '__main__':
    app.run(debug=True)
