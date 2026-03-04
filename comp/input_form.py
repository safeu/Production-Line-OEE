from dash import html, dcc
from database import get_all_machines


def create_input_form():
    return html.Div ([
        html.Label('Select Machine'),
        dcc.Dropdown(id='machine-selector', options=machine_selector(), value= None, style={
        'backgroundColor': '#16213e',
        'color': '#000000',
        'border': '1px solid #2a2a4a'
    }

),
        dcc.DatePickerSingle(id='shift-date', style={
        'backgroundColor': "#ffffff",
        'color': '#000000',
        'border': '1px solid #2a2a4a'
    }
),
        dcc.Dropdown(id='shift-selector', options=[{'label': 'Morning', 'value': 'morning'},
                                                   {'label': 'Afternoon', 'value': 'afternoon'},
                                                   {'label': 'Night', 'value': 'night'}], style={
        'backgroundColor': '#16213e',
        'color': '#000000',
        'border': '1px solid #2a2a4a'
    }

),
        dcc.Input(id='planned-production-time', type='number', placeholder = 'Enter planned production time (mins)'),
        dcc.Input(id='actual-run-time', type='number', placeholder = 'Enter actual run time (mins)'),
        dcc.Input(id='ideal-cycle-time', type='number', placeholder='Enter ideal cycle time (mins/unit)'),
        dcc.Input(id='total-units-produced', type='number', placeholder='Enter total units produced'),
        dcc.Input(id='good-units', type='number', placeholder='Enter good units'),
        html.Button('Submit', id='submit-button'),

        html.Hr(),
        html.P('Or import from CSV/Excel:'),
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag and Drop or ', html.A('Select File')]),
            style={
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'padding': '10px'
            }
            ),
        html.Div(id='upload-status')
    ])

def machine_selector():
    machines = get_all_machines()
    return [
        {'label': name, 'value': id } for id, name, department in machines
    ]
