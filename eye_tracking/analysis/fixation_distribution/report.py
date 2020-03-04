import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# TODO: define color palette
clrs=['blue', 'red']

def filter_fixations(data, format, confidence):
	"""
	Filter a dataframe of a specified format to return just the relevant data

	format: "gui", "events", or "samples"
	"""
	if format=='gui':
		cols = {"norm_pos_x": "x", "norm_pos_y": "y"}
		filtered= data[data['confidence']>=confidence].rename(columns=cols).query('x>=0 and x<=1 and y>=0 and y<=1')
		fix = filtered[['x', 'y', 'duration']]
	elif format=='events':
		cols= {"mean_gx":"x", "mean_gy":"y"}
		filtered=data[data['type']=="fixation"].rename(columns=cols).query('x>=0 and x<=1 and y>=0 and y<=1')
		fix = filtered[['x', 'y', 'duration']]
	elif format=='samples':
		cols={"gx":"x", "gy":"y"}
		filtered =data[data['type']=="fixation"]
		filtered = filtered[filtered['confidence']>=confidence].rename(columns=cols).query('x>=0 and x<=1 and y>=0 and y<=1')
		fix = filtered[['x', 'y']]

	return fix

def fixation_duration(df):
    ax=sns.pointplot(x="driving",y="duration",data=df, ci="sd", palette=clrs)
    plt.title("Average Fixation Duration")
    plt.show()
    fig = ax.get_figure()
    fig.savefig('average_fixation_duration.png')

def filter_saccades(data):
    return data.query("type == 'saccade' and amplitude <1")

def saccade_amplitude(df):
    ax=sns.pointplot(x="driving",y="amplitude",data=df, ci="sd", palette=clrs)
    plt.title("Average Saccade Amplitude")
    plt.show()
    fig = ax.get_figure()
    fig.savefig('average_saccade_amplitude.png')

def distance(row, center):
    return np.sqrt((row['x']-center[0])**2+(row['y']-center[1])**2)

def fixation_dispersion(df):
    ax=sns.pointplot(x="driving",y="dispersion",data=df, ci="sd", palette=clrs)
    plt.title("Average Fixation Dispersion")
    plt.show()
    fig = ax.get_figure()
    fig.savefig('average_fixation_dispersion.png')

def fixation_position(df, autonomous=True, manual=True, duration=False):
    auto=df[df['driving']=='autonomous']
    man=df[df['driving']=='manual']

    if duration:
        if autonomous:
            plt.scatter(x='x', y='y', s='duration', data=auto, color='blue', label='autonomous', alpha=0.1)
        if manual: 
            plt.scatter(x='x', y='y', s='duration', data=man, color='red', label='manual', alpha=0.1)
        plt.title("Fixation Position (size weighted by duration)")
    else: 
        if autonomous:
            plt.scatter(x='x', y='y', data=auto, color='blue', label='autonomous', alpha=0.1)
        if manual:
            plt.scatter(x='x', y='y', data=man, color='red', label='manual', alpha=0.1)
        plt.title("Fixation Position")
    
    plt.legend()
    plt.savefig('fixation_position.png')
    plt.show()

def run():
    auto_data = pd.read_csv("fixations_autonomous.csv")
    auto_fixations = filter_fixations(auto_data, "gui", 0.8)
    manual_data = pd.read_csv("fixations_manual.csv")
    manual_fixations = filter_fixations(manual_data, "gui", 0.8)
    auto_fixations['driving']='autonomous'
    manual_fixations['driving']='manual'
    fixations = pd.concat([auto_fixations, manual_fixations], ignore_index=True)

    ##Average Fixation Duration
    fixation_duration(fixations)

    ##Fixation Position 
    fixation_position(fixations, duration=True)

    ##Average Fixation Distance from Central Point
    auto_center = (np.mean(auto_fixations['x']), np.mean(auto_fixations['y']))
    manual_center = (np.mean(manual_fixations['x']), np.mean(manual_fixations['y']))

    auto_fixations['dispersion'] = auto_fixations.apply(distance, args=[auto_center], axis=1)
    manual_fixations['dispersion'] = manual_fixations.apply(distance, args=[manual_center], axis=1)

    fixations = pd.concat([auto_fixations, manual_fixations], ignore_index=True)
    fixation_dispersion(fixations)

    ##Average Saccade Amplitude
    auto_events = pd.read_csv("pl_events_autonomous.csv")
    auto_saccades = filter_saccades(auto_events)
    auto_saccades['driving']='autonomous'

    manual_events = pd.read_csv("pl_events_manual.csv")
    manual_saccades = filter_saccades(manual_events)
    manual_saccades['driving']='manual'

    saccades = pd.concat([auto_saccades,manual_saccades], ignore_index=True)
    saccade_amplitude(saccades)

run()

def grid_fixations(fixations):
    fixations['grid_x'] = np.floor(fixations['x']*grid_size[0])
    fixations['grid_y'] = np.floor(fixations['y']*grid_size[1])
    fixations = fixations.groupby(['grid_x', 'grid_y']).size().reset_index(level=['grid_x', 'grid_y'], name='num')
    
    blank_data = []
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            blank_data.append([x,y,0])
    blank = pd.DataFrame(blank_data, columns = ['grid_x', 'grid_y','num']) 
    
    fixations = fixations.append(blank, ignore_index=True)
    return fixations.groupby(['grid_x', 'grid_y']).sum().reset_index(level=['grid_x', 'grid_y'])

def t_test(a,b):
    t, p = stats.ttest_ind(a,b)
    print("t = ", t)
    print("p = ", p)