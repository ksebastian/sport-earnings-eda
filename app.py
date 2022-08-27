import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import pandas as pd
from random import randrange

###### Define your variables #####
tabtitle = 'Sport Earnings Worldwide'
color_list = ['paleturquoise', 'lavenderblush', 'aliceblue', 'burlywood', 'deeppink', 'lightyellow', 'beige',
              'greenyellow', 'darkorange']
sourceurl = 'https://github.com/ksebastian/sport-earnings-eda/blob/main/data/forbesathletesv2.csv'
githublink = 'https://github.com/ksebastian/sport-earnings-eda'

###### Import a dataframe #######
df = pd.read_csv("data/forbesathletesv2.csv")
selection_list = ['Top Sports']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose the category to visualize:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in selection_list],
        value=selection_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(category):
    top_sports_df = df.groupby('Sport')['Earnings'].mean().sort_values(ascending=False)

    top_sports_bar = go.Bar(x=top_sports_df.index,
                            y=top_sports_df,
                            name='Top Sports',
                            marker=dict(color=color_list[randrange(9)]))

    pagelayout = go.Layout(
        title='Sports Earnings',
        yaxis=dict(title='Earnings'),  # y-axis label
        xaxis=dict(title=str(category)),  # x-axis label

    )
    fig = go.Figure(data=top_sports_bar, layout=pagelayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
