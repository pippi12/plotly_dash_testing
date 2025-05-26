# %%
import dash
import dash_bootstrap_components as dbc
import dash.html as html  # 推奨されるインポート方法
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
import pandas as pd
import seaborn as sns
import dash_core_components as dcc

df = sns.load_dataset("titanic")

vars_cat = [var for var in df.columns if var.startswith('sex')]
vars_cont = [var for var in df.columns if var.startswith('age')]

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])
sidebar = html.Div(
    [
        dbc.Row(
            [
                html.H5('Settings',
                        style={'margin-top': '12px', 'margin-left': '24px'})
                ],
            style={"height": "5vh"},
            className='bg-primary text-white font-italic'
            ),
        dbc.Row(
            [
                html.Div([
                    html.P('Categorical Variable',
                           style={'margin-top': '8px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='my-cat-picker', multi=False, value='cat0',
                                 options=[{'label': x, 'value': x}
                                          for x in vars_cat],
                                 style={'width': '320px'}
                                 ),
                    html.P('Continuous Variable',
                           style={'margin-top': '16px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='my-cont-picker', multi=False, value='cont0',
                                 options=[{'label': x, 'value': x}
                                          for x in vars_cont],
                                 style={'width': '320px'}
                                 ),
                    html.P('Continuous Variables for Correlation Matrix',
                           style={'margin-top': '16px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='my-corr-picker', multi=True,
                                 value=vars_cont + ['target'],
                                 options=[{'label': x, 'value': x}
                                          for x in vars_cont + ['target']],
                                 style={'width': '320px'}
                                 ),
                    html.Button(id='my-button', n_clicks=0, children='apply',
                                style={'margin-top': '16px'},
                                className='bg-dark text-white'),
                    html.Hr()
                    ]
                    )
                ],
            style={'height': '50vh', 'margin': '8px'}),
        dbc.Row(
            [
                html.P('Target Variables', className='font-weight-bold')
                ],
            style={"height": "45vh", 'margin': '8px'}
            )
        ]
    )
content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Distribution of Categorical Variable'),
                        ],
                    className='bg-white'
                    ),
                dbc.Col(
                    [
                        html.P('Distribution of Continuous Variable')
                    ],
                    className='bg-dark text-white'
                    )
            ],
            style={"height": "50vh"}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Correlation Matrix Heatmap')
                    ],
                    className='bg-light'
                    )
            ],
            style={"height": "50vh"}
            )
        ]
    )
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className='bg-light'),
                dbc.Col(content, width=9)
            ],
        ),
    ],
    fluid=True
)

if __name__ == "__main__":

    # %%
    app.run_server(debug=True, port=1234)
# %%
