# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 15:48:35 2023

@author: phata
"""

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components

import dash

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])

app.layout = html.Div([
	html.H1('Multi-page app with Dash Pages'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", 
                    href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)