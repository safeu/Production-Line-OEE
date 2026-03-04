import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from plotly.tools import mpl_to_plotly


def plot_by_machine_bar(grouped_df):
    figure, ax = plt.subplots()
    ax.bar(grouped_df.index, grouped_df['oee'], color='#7b2fff')
    ax.set_title('OEE per machine')
    ax.set_xlabel('Machine ID')
    ax.set_ylabel('OEE')

    figure.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')
    ax.tick_params(colors='#a0a0b0')
    ax.xaxis.label.set_color('#a0a0b0')
    ax.yaxis.label.set_color('#a0a0b0')
    ax.title.set_color('#9d4edd')
    for spine in ax.spines.values():
        spine.set_edgecolor('#2a2a4a')

    return mpl_to_plotly(figure)

def plot_oee_trend(df):
    figure, ax = plt.subplots()
    colors = ['#7b2fff', '#9d4edd', '#c77dff']  # purple shades per machine
    for i, (machine_id, group) in enumerate(df.groupby('machine_id')):
        ax.plot(group['shift_date'], group['oee'], 
            label=f'Machine {machine_id}', 
            color=colors[i % len(colors)])
    ax.set_title('OEE over time')
    ax.set_xlabel('Shift Date')
    ax.set_ylabel('OEE')
    ax.legend()

    ax.tick_params(axis='x', rotation=45)
    return mpl_to_plotly(figure)

def plot_comp_breakdown(df):
    figure, ax = plt.subplots()
    ax.bar(['availability', 'performance', 'quality'], 
           [df['availability'].mean(), df['performance'].mean(), df['quality'].mean()])
    ax.set_title('Component Breakdown')
    ax.set_xlabel('Components')
    ax.set_ylabel('Average Values')

    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(['Availability', 'Performance', 'Quality'])

    figure.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')
    ax.tick_params(colors='#a0a0b0')
    ax.xaxis.label.set_color('#a0a0b0')
    ax.yaxis.label.set_color('#a0a0b0')
    ax.title.set_color('#9d4edd')
    for spine in ax.spines.values():
        spine.set_edgecolor('#2a2a4a')

    return mpl_to_plotly(figure)