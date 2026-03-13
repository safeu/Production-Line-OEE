from dash import html, dcc

def create_dashboard():
    return html.Div([
        html.Div([
            html.Div("LIVE ", id='dashboard-status'),
            html.Button("Refresh", id='refresh-button', n_clicks=0),
        ], id='dashboard-toolbar'),

         html.Div([
            _kpi('OEE', 'oee-kpi', '—', '%', 'Overall'),
            _kpi('Availability', 'avail-kpi', '—', '%', 'A-factor'),
            _kpi('Performance', 'perf-kpi', '—', '%', 'P-factor'),
            _kpi('Quality', 'qual-kpi', '—', '%', 'Q-factor'),
        ], id='kpi-row'),

        html.Div([
            html.Div([
                html.Div([
                    html.Div("OEE per Machine", className='chart-title'),
                    html.Div(className='chart-dot'),
                ], className='chart-header'),
                dcc.Graph(id='by-machine-bar', config={'displayModeBar': False},
                        style={'height': '260px'}),
            ], className='chart-card'),

            html.Div([
                html.Div([
                    html.Div('Component Breakdown', className='chart-title'),
                    html.Div(className='chart-dot'),
                ], className='chart-header'),
                dcc.Graph(id='comp-breakdown', config={'displayModeBar': False},
                            style={'height': '260px'}),
            ], className='chart-card'),

            html.Div([
                html.Div([
                    html.Div('OEE Trend over Time', className='chart-title'),
                    html.Div(className='chart-dot'),
                ], className='chart-header'),
                dcc.Graph(id='oee-trend', config={'displayModeBar': False},
                        style={'height': '260px'}),
            ], className='chart-card full-width'),
        
        ], id='charts-grid')
    ], id='dashboard-container')


def _kpi(label, elem_id, value, unit, sub):
    return html.Div([
        html.Div(label, className='kpi-label'),
        html.Div([value, html.Span(f' {unit}')], className='kpi-value', id=elem_id),
        html.Div(sub, className='kpi-sub'),
    ], className='kpi-card')