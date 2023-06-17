from flask import Flask, render_template
import pandas as pd

import scatter_chart.gen_data as scatter_data

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
    data = {
        'labels': [
            'Eating',
            'Drinking',
            'Sleeping',
            'Designing',
            'Coding',
            'Cycling',
            'Running'
        ],
        'datasets': [{
            'label': 'My First Dataset',
            'data': [65, 59, 90, 81, 56, 55, 40],
            'fill': True,
            'backgroundColor': 'rgba(255, 99, 132, 0.2)',
            'borderColor': 'rgb(255, 99, 132)',
            'pointBackgroundColor': 'rgb(255, 99, 132)',
            'pointBorderColor': '#fff',
            'pointHoverBackgroundColor': '#fff',
            'pointHoverBorderColor': 'rgb(255, 99, 132)'
        }, {
            'label': 'My Second Dataset',
            'data': [28, 48, 40, 19, 96, 27, 100],
            'fill': True,
            'backgroundColor': 'rgba(54, 162, 235, 0.2)',
            'borderColor': 'rgb(54, 162, 235)',
            'pointBackgroundColor': 'rgb(54, 162, 235)',
            'pointBorderColor': '#fff',
            'pointHoverBackgroundColor': '#fff',
            'pointHoverBorderColor': 'rgb(54, 162, 235)'
        }]
    }

    config = {
        'type': 'radar',
        'data': data,
        'options': {
            'elements': {
                'line': {
                    'borderWidth': 3
                }
            }
        },
    }

    return config

def getChartInfo3():
    data = {
        'datasets': [{
            'label': 'First Dataset',
            'data': [{
                'x': 20,
                'y': 30,
                'r': 15
            }, {
                'x': 40,
                'y': 10,
                'r': 10
            }],
            'backgroundColor': 'rgb(255, 99, 132)'
        }]
    }
    
    config = {
        'type': 'bubble',
        'data': data,
        'options': {}
    }

    return config

if __name__ == '__main__':
    app.run(debug=True)
