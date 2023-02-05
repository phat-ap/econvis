from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

# Build App
app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])

# layout
app.layout = dbc.Container([mytitle, mygraph, dropdown])

# Run app and display result inline in the notebook
app.run_server()