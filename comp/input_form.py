from dash import html, dcc
from database import get_all_machines


def create_input_form():
    machines = get_all_machines() or []
    machine_options = [{'label': f'#{m[0]}  {m[1]}', 'value': m[0]} for m in machines]
    
    return html.Div([
        html.Div('Machine', className ='form-section-label'),
        html.Label('Select Machine'),
        dcc.Dropdown(id='machine-selector', options=machine_options,
                     placeholder='Select machine...',
                     style ={'fontSize': '13px'}),


        html.Div('Shift', className='form-section-label'),
        html.Label('Data'),
        dcc.DatePickerSingle(id='shift-date', placeholder='YYYY-MM-DD',
                             display_format='YYYY-MM-DD',
                             style ={'width': '100%'}),
        
        html.Label('Shift'),
        dcc.Dropdown(id='shift-selector',
                     options=[
                         {'label': 'Morning', 'value':'morning'},
                         {'label': 'Afternoon', 'value':'afternoon'},
                         {'label': 'Night', 'value':'night'},
                     ], placeholder='Select shift',
                     ),

        html.Div('Production Data', className='form-section-label'),
 
        html.Label('Planned Production Time (min)'),
        dcc.Input(id='planned-production-time', type='number', placeholder='e.g. 480',
                  style={'width': '100%'}),
 
        html.Label('Actual Run Time (min)'),
        dcc.Input(id='actual-run-time', type='number', placeholder='e.g. 440',
                  style={'width': '100%'}),
 
        html.Label('Ideal Cycle Time (min/unit)'),
        dcc.Input(id='ideal-cycle-time', type='number', placeholder='e.g. 0.5',
                  style={'width': '100%'}),
 
        html.Label('Total Units Produced'),
        dcc.Input(id='total-units-produced', type='number', placeholder='e.g. 800',
                  style={'width': '100%'}),
 
        html.Label('Good Units'),
        dcc.Input(id='good-units', type='number', placeholder='e.g. 780',
                  style={'width': '100%'}),
 
        html.Button('→  Submit Log', id='submit-button', n_clicks=0),

        
        html.Div('Bulk Import', className='form-section-label'),

        dcc.Upload(
            id='upload-data',
            children=html.Div([
                html.Div('Drag & Drop or Click', style={
                    'fontFamily': 'IBM Plex Mono, monospace',
                    'fontSize': '11px',
                    'color': '#3d4255',
                    'letterSpacing': '0.05em'
                }),
                html.Div('CSV / Excel', style={
                    'fontFamily': 'IBM Plex Mono, monospace',
                    'fontSize': '10px',
                    'color': '#2a1f4a',
                    'marginTop': '3px',
                    'letterSpacing': '0.01em'}),
            ]), multiple=False),
    html.Div(id='upload-status'),
])