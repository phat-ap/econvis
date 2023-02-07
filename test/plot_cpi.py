from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import pandas as pd

# Data
df_cpi = pd.read_csv('https://raw.githubusercontent.com/phat-ap/econvis/main/Data/tha_cpi.csv',
                     parse_dates=['date'],
                     index_col=['date'])

# Build App
app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
mytitle = dcc.Markdown(children='# Thailand Inflation')

# Checklist
cl_cpi = dcc.Checklist(df_cpi.columns, df_cpi.columns[0], labelStyle={'display': 'block'})
# Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_cpi.index, y=df_cpi.CPI,
                    mode='lines',
                    name='lines'))
fig.add_trace(go.Scatter(x=df_cpi.index, y=df_cpi.Eggs,
                    mode='lines',
                    name='lines'))

mygraph = dcc.Graph(figure=fig)

mytext = dcc.Markdown(children='')


# layout
app.layout = dbc.Container([mytitle, mygraph, cl_cpi, mytext])

# Interactivity

@app.callback(
    Output(mytext, component_property='children'),
    Input(cl_cpi, component_property='value')
)
def update_graph(user_input):  # function arguments come from the component property of the Input
    return ' '.join(user_input)  # returned objects are assigned to the component property of the Output

# Run app
if __name__=='__main__':
    app.run_server()