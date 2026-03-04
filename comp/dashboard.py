from dash import html, dcc

def create_dashboard():
    return html.Div([
        html.Button('Refresh Charts', id='refresh-button'),
        html.Div(id='refresh-status'),
        dcc.Graph(id='by-machine-bar'),
        dcc.Graph(id='oee-trend'),
        dcc.Graph(id='comp-breakdown'),
        html.Div(id='oee-summary', style={'display': 'flex', 'justifyContent': 'space-around'})
    ])