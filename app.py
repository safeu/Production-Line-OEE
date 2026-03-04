from dash import Dash, html, Input, Output, State
from comp.input_form import create_input_form
from comp.dashboard import create_dashboard
from database import create_tables, add_log, get_logs
from oee import compute_for_oee, get_oee_by_machine
from charts import plot_by_machine_bar, plot_oee_trend, plot_comp_breakdown
import base64
import io
import pandas as pd
import traceback


app = Dash(__name__)
create_tables()
app.layout = html.Div([
    html.H1('Production Line OEE Dashboard', 
            style={'textAlign': 'center', 'color': '#9d4edd'}),
    html.P('Track and analyze Overall Equipment Effectiveness', 
           style={'textAlign': 'center', 'color': '#a0a0b0'}),
    html.Div([
        html.Div(create_input_form(), id='form-container'),
        html.Div(create_dashboard(), id='dashboard-container')
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'gap': '20px',
        'alignItems': 'flex-start'
    })
])


@app.callback(
    Output('by-machine-bar', 'figure'),
    Output('oee-trend', 'figure'),
    Output('comp-breakdown', 'figure'),
    Input('submit-button', 'n_clicks'), 
    Input('refresh-button', 'n_clicks'),
    State('machine-selector', 'value'),
    State('shift-date', 'date'),
    State('shift-selector', 'value'),
    State('planned-production-time', 'value'),
    State('actual-run-time', 'value'),
    State('ideal-cycle-time', 'value'),
    State('total-units-produced', 'value'),
    State('good-units', 'value'),
)

def update_dashboard(submit_clicks, refresh_clicks, machine_id, shift_date, shift, 
                     planned_time, actual_run_time, ideal_cycle_time, 
                     total_units, good_units):
    if submit_clicks is None and refresh_clicks is None:
        logs = get_logs()
        if not logs:
            return {}, {}, {}
        df = compute_for_oee(logs)
        grouped_df = get_oee_by_machine(df)
        return plot_by_machine_bar(grouped_df), plot_oee_trend(df), plot_comp_breakdown(df)

    try:    
        if submit_clicks:
            add_log(machine_id, shift_date, shift, planned_time, 
                actual_run_time, ideal_cycle_time, total_units, good_units)
            
        logs = get_logs()
        df = compute_for_oee(logs)
        grouped_df = get_oee_by_machine(df)
        figure_1 = plot_by_machine_bar(grouped_df)
        figure_2 = plot_oee_trend(df)
        figure_3 = plot_comp_breakdown(df)

        return figure_1, figure_2, figure_3
    except Exception as e:
        print(traceback.format_exc())
        return {}, {}, {}

@app.callback(
    Output('upload-status', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)

def handle_upload(contents, filename):
    if contents is None:
        return ''
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))

        for _, row in df.iterrows():
            print(row)
            add_log(row['machine_id'], row['shift_date'], row['shift'],
                    row['planned_production_time'], row['actual_run_time'], row['ideal_cycle_time'],
                    row['total_units_produced'], row['good_units'])

        return "File uploaded successfully"

    except Exception as e:
        return f"Error uploading file: {e}"




if __name__ == '__main__':
    app.run(debug=True)