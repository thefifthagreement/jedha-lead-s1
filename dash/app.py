import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import boto3

external_stylesheets = ['https://cdn.jsdelivr.net/npm/bulma@0.9.0/css/bulma.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# read data
with open('aws-cred.json') as json_data_file:
            config = json.load(json_data_file)

session = boto3.Session(
    aws_access_key_id=config["ACCESS_KEY_ID"],
    aws_secret_access_key=config["SECRET_ACCESS_KEY"],
    region_name='eu-west-3'
    )

s3 = session.client("s3")
s3.download_file('lead-us-car', 'final_v2/us_car_accident_grouped.csv', './us_car_accident_grouped.csv')

df = pd.read_csv("./us_car_accident_grouped.csv")

# app layout

app.layout = html.Div(children=[
    html.Center(children=[
        html.H1(children='US car accident frequency heatmap.', className='title is-1'),
        dcc.Markdown("""
        Representing the distribution of the United States car accidents.

        Using **Docker** and **Dash**.
        """)
    ]),
    html.Div(
        children=[
            dcc.Graph(
                id='us-car-accident-distribution-graph'
            ),
            dcc.Slider(
                id='year-slider',
                min=df['year'].min(),
                max=df['year'].max(),
                value=df['year'].max(),
                marks={str(year): str(year) for year in df['year'].unique()},
                step=None
            )
        ],
        className='section'
    )
], className='section')

@app.callback(
    Output('us-car-accident-distribution-graph', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_year):
    # filtering the data using the chosen year
    filtered_df = df[df["year"] <= selected_year]

    fig = go.Figure(data=go.Choropleth(
        locations=df['State'], # Spatial coordinates
        z = filtered_df['count'].astype("float"), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        autocolorscale = False,
        colorscale = 'Reds',
        colorbar_title = "Total car accident",
    ))

    fig.update_layout(
        title_text = f'US car accidents distribution by States from 2016 to {selected_year}.',
        geo_scope='usa', # limite map scope to USA
    )

    return fig

if __name__ == '__main__':
  app.run_server(host='0.0.0.0', debug=True)