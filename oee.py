import pandas as pd


def compute_for_oee(logs):
    columns = ['id', 'machine_id', 'shift_date', 'shift', 
               'planned_production_time', 'actual_run_time', 
               'ideal_cycle_time', 'total_units_produced', 'good_units']
    
    df = pd.DataFrame(logs, columns=columns)
    df['shift_date'] = pd.to_datetime(df['shift_date'])
    
    if df.empty:
        return df
    
    df['availability'] = df['actual_run_time'] / df['planned_production_time']
    df['performance'] = (df['ideal_cycle_time']*df['total_units_produced']) / df['actual_run_time']
    df['quality'] = df['good_units'] / df['total_units_produced']

    df['oee'] = df['availability'] * df['performance'] * df['quality']

    return df

def get_oee_summary(df):
    return {
        'availability': df['availability'].mean(),
        'performance': df['performance'].mean(),
        'quality': df['quality'].mean(),
        'oee': df['oee'].mean()
    }

def get_oee_by_machine(df):
    return df.groupby('machine_id')[['availability', 'performance', 'quality', 'oee']].mean()