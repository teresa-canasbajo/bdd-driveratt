import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# TODO: define color palette
clrs=['blue', 'red']

############
# PROCESSING
############
def filter_fixations(data, format):
	"""
	Filter a dataframe of a specified format to return just the relevant data

	format: "gui", "events", or "samples"
	"""
	if format=='gui':
		cols = {"norm_pos_x": "x", "norm_pos_y": "y"}
		filtered= data[data['confidence']>=0.8].rename(columns=cols).query('x>=0 and x<=1 and y>=0 and y<=1')
		fix = filtered[['x', 'y', 'duration']]
	elif format=='events':
		cols= {"mean_gx":"x", "mean_gy":"y"}
		filtered=data[data['type']=="fixation"].rename(columns=cols).query('x>=0 and x<=1 and y>=0 and y<=1')
		fix = filtered[['x', 'y', 'duration']]
	elif format=='samples':
		cols={"gx":"x", "gy":"y"}
		filtered =data[data['type']=="fixation"]
		filtered = filtered[filtered['confidence']>=0.8].rename(columns=cols).query('x>=0 and x<=1 and y>=0 and y<=1')
		fix = filtered[['x', 'y']]

	return fix

def filter_saccades(data):
    return data.query("type == 'saccade' and amplitude <1")

def distance(row, center):
    return np.sqrt((row['x']-center[0])**2+(row['y']-center[1])**2)

def processObserverFixations(filename, label, drivingType):
    raw_data = pd.read_csv(filename)
    fix = filter_fixations(raw_data, "gui")
    duration = np.mean(fix['duration'])
    center = (np.mean(fix['x']), np.mean(fix['y']))
    fix['dispersion'] = fix.apply(distance, args=[center], axis=1)
    dispersion = np.mean(fix['dispersion'])
    return [label, drivingType, duration, dispersion]

def processObserverSaccades(filename, label, drivingType):
    raw_data = pd.read_csv(filename)
    saccades = filter_saccades(raw_data)
    return [label, drivingType, np.mean(saccades['amplitude'])]

############
# PLOTS
############
def plot_fixation_duration(df):
    ax=sns.pointplot(x="driving",y="duration",data=df, ci="sd", palette=clrs)
    plt.title("Average Fixation Duration")
    plt.show()
    fig = ax.get_figure()
    fig.savefig('average_fixation_duration.png')

def plot_fixation_dispersion(df):
    ax=sns.pointplot(x="driving",y="dispersion",data=df, ci="sd", palette=clrs)
    plt.title("Average Fixation Dispersion")
    plt.show()
    fig = ax.get_figure()
    fig.savefig('average_fixation_dispersion.png')

def plot_saccade_amplitude(df):
    ax=sns.pointplot(x="driving",y="amplitude",data=df, ci="sd", palette=clrs)
    plt.title("Average Saccade Amplitude")
    plt.show()
    fig = ax.get_figure()
    fig.savefig('average_saccade_amplitude.png')

def generatePlots(data):
    ##Average Fixation Duration
    plot_fixation_duration(data)   
    #Average Fixation Distance from Central Point
    plot_fixation_dispersion(data)
    #Average Saccade Amplitude
    plot_saccade_amplitude(data)


############

############
def t_test(a,b):
    t, p = stats.ttest_ind(a,b)
    return t, p

############
# run report
############
def run():
    fixation_files = pd.read_csv("fixation_files.csv")
    fixation_data = pd.DataFrame(columns={'obs', 'driving', 'duration', 'dispersion'})
    fixation_data=fixation_data[['obs','driving','duration','dispersion']]

    for index in range(len(fixation_files)):
        file = fixation_files.loc[index]
        filename = file['filename']
        observer = file['observerId']
        driving= file['drivingType']

        fix = processObserverFixations(filename, observer, driving)
        fixation_data.loc[len(fixation_data)] = fix

    event_files = pd.read_csv("event_files.csv")
    saccade_data = pd.DataFrame(columns={'obs', 'driving', 'amplitude'})
    saccade_data=saccade_data[['obs','driving','amplitude']]
        
    for index in range(len(event_files)):
        file = event_files.loc[index]
        filename = file['filename']
        observer = file['observerId']
        driving = file['drivingType']

        sacc = processObserverSaccades(filename, observer, driving)
        saccade_data.loc[len(saccade_data)]=sacc

    master_data = fixation_data.merge(saccade_data, on=['obs', 'driving'])
    generatePlots(master_data)

run()