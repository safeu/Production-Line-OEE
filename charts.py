import plotly.express as px
import plotly.graph_objects as go

BG_MAIN    = '#0e1117'
BG_CARD    = '#131720'
ACCENT     = '#7b2fff'
ACCENT_MID = '#9d4edd'
ACCENT_LT  = '#c084fc'
TEXT_PRI   = '#e8eaf0'
TEXT_SEC   = '#6b7080'
TEXT_MUT   = '#3d4255'
BORDER     = '#1c2030'
SUCCESS    = '#22c55e'
WARNING    = '#f59e0b'

MACHINE_COLORS = ['#7b2fff', '#c084fc', '#38bdf8', '#f472b6', '#fb923c']

XAXIS_BASE = dict(
    gridcolor=BORDER,
    linecolor=BORDER,
    tickcolor=BORDER,
    tickfont=dict(size=10, color=TEXT_MUT),
    showgrid=False,
    zeroline=False,
)
YAXIS_BASE = dict(
    gridcolor=BORDER,
    linecolor='rgba(0,0,0,0)',
    tickcolor='rgba(0,0,0,0)',
    tickfont=dict(size=10, color=TEXT_MUT),
    gridwidth=1,
    showgrid=True,
    zeroline=False,
)
LAYOUT_BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='IBM Plex Mono, monospace', color=TEXT_SEC, size=11),
    margin=dict(l=48, r=20, t=20, b=48),
    xaxis=XAXIS_BASE,
    yaxis=YAXIS_BASE,
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        bordercolor=BORDER,
        borderwidth=1,
        font=dict(size=10, color=TEXT_SEC),
    ),
    hoverlabel=dict(
        bgcolor='#1a1f2e',
        bordercolor=BORDER,
        font=dict(family='IBM Plex Mono, monospace', size=11, color=TEXT_PRI),
    ),
)


def _oee_color(val):
    if val >= 0.85:
        return SUCCESS
    elif val >= 0.60:
        return WARNING
    return '#ef4444'


def _empty_fig(msg='No data'):
    fig = go.Figure()
    fig.add_annotation(
        text=msg, x=0.5, y=0.5,
        xref='paper', yref='paper',
        showarrow=False,
        font=dict(family='IBM Plex Mono, monospace', size=12, color=TEXT_MUT),
    )

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      xaxis=dict(visible=False),
                      yaxis=dict(visible=False),
                      margin=dict(l=0, r=0, t=0, b=0),
                      )
    return fig


def plot_by_machine_bar(grouped_df):
    if grouped_df is None or grouped_df.empty:
        return _empty_fig("No data yet")
    
    machines = [f'M{i}' for i in grouped_df.index]
    values = grouped_df['oee'].tolist()
    colors = [_oee_color(v) for v in values]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=machines, y=values, marker=dict(
        color=colors, opacity= 0.85, line=dict(width=0),
    ),
    customdata=[[f'{v*100: .1f}%'] for v in values],
    hovertemplate='<b>%{x}</b><br>OEE: %{customdata[0]}<extra></extra>',
    width=0.5,
    ))

    fig.add_hline(y=0.85, line=dict(color=SUCCESS, width=1, dash='dot'),
                    annotation_text='85% target',
                    annotation_font=dict(size=9, color=TEXT_MUT),
                    annotation_position='top right',)
    
    layout = dict(**LAYOUT_BASE)
    layout['yaxis'] = dict(**YAXIS_BASE, tickformat='.0%', range=[0, 1.05])
    fig.update_layout(**layout)
    return fig


def plot_oee_trend(df):
    if df is None or df.empty:
        return _empty_fig("No data yet")
    
    fig = go.Figure()

    for i, (machine_id, group) in enumerate(df.groupby('machine_id')):
        color = MACHINE_COLORS[i % len(MACHINE_COLORS)]
        group_sorted = group.sort_values('shift_date')

        fig.add_trace(go.Scatter(
            x=group_sorted['shift_date'],
            y=group_sorted['oee'],
            mode='lines+markers',
            name=f'Machine {machine_id}',
            line=dict(color=color, width=2),
            marker=dict(size=5, color=color, line=dict(width=1, color=BG_CARD)),
            hovertemplate= f'<b>Machine {machine_id}</b><br>Date: %{{x|%Y-%m-%d}}<br>OEE: %{{y:.1%}}<extra></extra>',
        ))

    fig.add_hline(y=0.85, line=dict(color=SUCCESS, width=1, dash='dot'))

    layout = dict(**LAYOUT_BASE)
    layout['yaxis'] = dict(**YAXIS_BASE, tickformat='.0%', range=[0, 1.05])
    layout['xaxis'] = dict(**XAXIS_BASE, tickformat='%b %d')
    fig.update_layout(**layout)
    return fig


def plot_comp_breakdown(df):
        if df is None or df.empty:
            return _empty_fig('No data yet')
 
        components = ['Availability', 'Performance', 'Quality']
        values = [
            df['availability'].mean(),
            df['performance'].mean(),
            df['quality'].mean(),
        ]
        colors = [_oee_color(v) for v in values]
    
        fig = go.Figure()
        fig.add_trace(go.Bar(x=components, y=values, marker=dict(
                color=colors,
                opacity=0.85,
                line=dict(width=0),
            ),
            customdata=[[f'{v*100:.1f}%'] for v in values],
            hovertemplate='<b>%{x}</b><br>Avg: %{customdata[0]}<extra></extra>',
            width=0.45,
        ))
    
        fig.add_hline(
            y=0.85,
            line=dict(color=SUCCESS, width=1, dash='dot'),
            annotation_text='85%',
            annotation_font=dict(size=9, color=TEXT_MUT),
            annotation_position='top right',
        )
    
        layout = dict(**LAYOUT_BASE)
        layout['yaxis'] = dict(**YAXIS_BASE, tickformat='.0%', range=[0, 1.05])
        fig.update_layout(**layout)
        return fig


