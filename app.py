from dash import Dash, html, dcc, Input, Output, State
from comp.input_form import create_input_form
from comp.dashboard import create_dashboard
from database import create_tables, add_log, get_logs
from oee import compute_for_oee, get_oee_by_machine, get_oee_summary
from charts import plot_by_machine_bar, plot_oee_trend, plot_comp_breakdown
import base64
import io
import pandas as pd
import traceback


app = Dash(__name__)
create_tables()

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1("PRODUCTION LINE OEE"),
            html.Div('v1.0', id='header-badge'),
        ], id='header-left'),
    html.P("Overall Equipment Effectiveness"),
    ], id='header'),

    html.Div([
        html.Div(create_input_form(), id='form-container'),
        create_dashboard()
    ], id='main-layout'),
])

@app.callback(
    Output('by-machine-bar', 'figure'),
    Output('oee-trend', 'figure'),
    Output('comp-breakdown', 'figure'),
    Output('oee-kpi', 'children'),
    Output('avail-kpi', 'children'),
    Output('perf-kpi', 'children'),
    Output('qual-kpi', 'children'),
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
    
    empty_kpi = ['-', '-', '-', '-']

    def _kpi_val(v):
        from dash import html as h
        return [f'{v*100:.1f}', h.Span(' %')]


    try:    
        if submit_clicks:
            add_log(machine_id, shift_date, shift, planned_time, 
                actual_run_time, ideal_cycle_time, total_units, good_units)
            
        logs = get_logs()
        if not logs:
            from charts import _empty_fig
            ef = _empty_fig('Submit a log to get started')
            return ef, ef, ef, *empty_kpi


        df = compute_for_oee(logs)
        grouped_df = get_oee_by_machine(df)
        summary = get_oee_summary(df)

        return (
            plot_by_machine_bar(grouped_df),
            plot_oee_trend(df),
            plot_comp_breakdown(df),
            _kpi_val(summary['oee']),
            _kpi_val(summary['availability']),
            _kpi_val(summary['performance']),
            _kpi_val(summary['quality'])
        )
    

    except Exception as e:
        print(traceback.format_exc())
        from charts import _empty_fig
        ef = _empty_fig("Error Loading data")
        return ef, ef, ef, *empty_kpi


@app.callback(
    Output('upload-status', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)

def handle_upload(contents, filename):
    if contents is None:
        return ''
    try:
        _, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
 
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return '✗  Unsupported file type'
 
        from database import database_connection
        conn = database_connection()
        cursor = conn.cursor()

        for _, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO production_logs
                    (machine_id, shift_date, shift, planned_production_time,
                     actual_run_time, ideal_cycle_time, total_units_produced, good_units)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (row['machine_id'], row['shift_date'], row['shift'],
                      row['planned_production_time'], row['actual_run_time'],
                      row['ideal_cycle_time'], row['total_units_produced'], row['good_units']))

            except Exception as row_err:
                print(f"Skipping row: {row_err}")

        conn.commit()
        conn.close()
 
        return f'{filename} imported ({len(df)} rows)'
 
    except Exception as e:
        return f'Failed to import: {e}'


if __name__ == '__main__':
    app.run(debug=True)