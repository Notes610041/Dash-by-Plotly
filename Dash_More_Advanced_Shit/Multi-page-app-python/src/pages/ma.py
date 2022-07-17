import dash

dash.register_page(__name__, name='Massachusetts')

from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
import pathlib

# data from https://d2ln813o5uvqrd.cloudfront.net/
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
df = pd.read_csv(DATA_PATH.joinpath('MA-data.csv'))


def build_graph(dff):
    fig = go.Figure(layout_yaxis_range=[50, 200], layout_xaxis_range=[1950, 2099], layout_showlegend=False)
    fig.add_trace(go.Scatter(x=dff['Year'], y=dff['Modeled Mean']))
    fig.add_trace(go.Scatter(x=dff['Year'], y=dff['Modeled Min'], fill='tonexty',fillcolor='rgba(255, 0, 0, 0.7)'))
    fig.add_trace(go.Scatter(x=dff['Year'], y=dff['Modeled Max'], fill='tonexty',fillcolor='rgba(0, 230, 64, 0.1)'))
    fig.add_trace(go.Scatter(x=dff['Year'], y=dff['Days with Minimum Temperature Below 32°F'], mode='markers'))
    fig.update_layout(margin=dict(l=35, r=35, t=35, b=35), title="Annual Days with Minimum Temperature Below 32°F - Massachusetts")
    fig.update_yaxes(title_text='Days')
    return fig


layout = dbc.Row(
    [
        dbc.Col([
            html.Label("Emissions of GHG"),
            dcc.RadioItems(['Low', 'High'], value='High', id='emissions32',
                           labelStyle={'display': 'block'}),
        ], width=2),

        dbc.Col([
            dcc.Graph(id='my-graph32', animate=True,
                      animation_options={'transition': {'duration': 750,
                                                        'ease': 'cubic-in-out'}}),
        ], width=10)

    ]
)


@callback(
    Output('my-graph32', 'figure'),
    Input('emissions32', 'value'),
)
def render_content(value):
    if value == 'High':
        dff = df[df['RCP'] == 8.5]
        fig = build_graph(dff)
    else:
        dff = df[df['RCP'] == 4.5]
        fig = build_graph(dff)
    return fig
