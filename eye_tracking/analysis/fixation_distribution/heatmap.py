import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

### Run from command line
def heatmap_from_input():
	parser = argparse.ArgumentParser(description='Required parameters')

	#required args
	parser.add_argument('input-path', type=str, help='Path to the csv input')
	parser.add_argument('data-format', type=str, help='Format of the csv input')
	parser.add_argument('output-name', type=str,  help='Name of the output file')

	#optional args
	parser.add_argument('-a', '--alpha-value', type=float, default=0.5, required=False, help='Transparency level for the overlay')
	parser.add_argument('-c', '--confidence-level', type=float, default=0.8, required=False, help='Confidence level to filter by')
	parser.add_argument('-d','--duration-weight', type=bool, default=False, required=False, help='Whether fixation duration is taken into account as a weight')

	args = vars(parser.parse_args())

	#required args
	input_path = args['input-path']
	data_format = args['data-format']
	output_name = args['output-name']

	#optional args
	alpha_value=args['alpha_value']
	confidence_level = args['confidence_level']
	duration_weight=args['duration_weight']

	draw_heatmap(input_path, data_format, output_name, alpha_value, confidence_level, duration_weight)

def draw_heatmap(datapath, dataFormat, outputName, alpha=0.5, confidence=0.8, durationWeight=False): 
	data = pd.read_csv(datapath)
	fixations = filter_fixations(data, dataFormat, confidence)

	if durationWeight: 
		draw_heatmap_with_duration(fixations, dispsize=(200, 200), imagefile=None, alpha=alpha, savefilename=outputName)
	else:
		ax = sns.kdeplot(fixations['x'], fixations['y'], cmap="jet", n_levels = 50, shade=True, shadeLowest=False, alpha=alpha)
		plt.xlim(0, 1)
		plt.ylim(0, 1)
		plt.axis()
		plt.title("Distribution of eye movements from %s" % datapath)
		plt.show()
		fig = ax.get_figure()
		fig.savefig(outputName, transparent=False)

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

	totalPoints = len(data)
	filteredPoints = len(fix)
	percent = filteredPoints/totalPoints
	print("%f of data meets filtering " % percent)
	return fix


# adapted from PyGaze
def gaussian(x, sdx, y=None, sdy=None):
	
	"""Returns an array of numpy arrays (a matrix) containing values between
	1 and 0 in a 2D Gaussian distribution
	
	arguments
	x		-- width in pixels
	sdx		-- width standard deviation
	
	keyword argments
	y		-- height in pixels (default = x)
	sdy		-- height standard deviation (default = sdx)
	"""
	
	# square Gaussian if only x values are passed
	if y == None:
		y = x
	if sdy == None:
		sdy = sdx
	# centers	
	x_mid = x/2
	y_mid = y/2
	# matrix of zeros
	M = np.zeros([y,x],dtype=float)
	# gaussian matrix
	for i in range(x):
		for j in range(y):
			M[j,i] = np.exp(-1.0 * (((float(i)-x_mid)**2/(2*sdx*sdx)) + ((float(j)-y_mid)**2/(2*sdy*sdy)) ) )
	
	return M

# adapted from PyGaze
def draw_heatmap_with_duration(fixations, dispsize, imagefile=None, alpha=0.5, savefilename=None):
	
	"""Draws a heatmap of the provided fixations, optionally drawn over an
	image, and optionally allocating more weight to fixations with a higher
	duration.
	
	arguments
	
	fixations		-	a dataframe of fixation events 
	dispsize		-	tuple or list indicating the size of the display,
					e.g. (1024,768)
	
	keyword arguments
	
	imagefile		-	full path to an image file over which the heatmap
					is to be laid, or None for no image; NOTE: the image
					may be smaller than the display size, the function
					assumes that the image was presented at the centre of
					the display (default = None)
	durationweight	-	Boolean indicating whether the fixation duration is
					to be taken into account as a weight for the heatmap
					intensity; longer duration = hotter (default = True)
	alpha		-	float between 0 and 1, indicating the transparancy of
					the heatmap, where 0 is completely transparant and 1
					is completely untransparant (default = 0.5)
	savefilename	-	full path to the file in which the heatmap should be
					saved, or None to not save the file (default = None)
	
	returns
	
	fig			-	a matplotlib.pyplot Figure instance, containing the
					heatmap
	"""

	fig, ax = draw_display(dispsize, imagefile=imagefile)

	# HEATMAP
	# Gaussian
	gwh = 200
	gsdwh = gwh/6
	gaus = gaussian(gwh,gsdwh)
	# matrix of zeroes
	strt = gwh/2
	heatmapsize = int(dispsize[1] + 2*strt), int(dispsize[0] + 2*strt)
	heatmap = np.zeros(heatmapsize, dtype=float)
	# create heatmap
	for i in range(0,len(fixations['duration'])):
		# get x and y coordinates
		#x and y - indexes of heatmap array. must be integers
		x = int(strt) + int(fixations['x'].iloc[i]) - int(gwh/2)
		y = int(strt) + int(fixations['y'].iloc[i]) - int(gwh/2)
		# correct Gaussian size if either coordinate falls outside of
		# display boundaries
		if (not 0 < x < dispsize[0]) or (not 0 < y < dispsize[1]):
			hadj=[0,gwh]
			vadj=[0,gwh]
			if 0 > x:
				hadj[0] = abs(x)
				x = 0
			elif dispsize[0] < x:
				hadj[1] = gwh - int(x-dispsize[0])
			if 0 > y:
				vadj[0] = abs(y)
				y = 0
			elif dispsize[1] < y:
				vadj[1] = gwh - int(y-dispsize[1])
			# add adjusted Gaussian to the current heatmap
			try:
				heatmap[y:y+vadj[1],x:x+hadj[1]] += gaus[vadj[0]:vadj[1],hadj[0]:hadj[1]] * fixations['duration'].iloc[i]
			except:
				# fixation was probably outside of display
				pass
		else:				
			# add Gaussian to the current heatmap
			heatmap[y:y+gwh,x:x+gwh] += gaus * fixations['duration'].iloc[i]
	# resize heatmap
	# heatmap = heatmap[int(strt):int(dispsize[1]+strt),int(strt):int(dispsize[0]+strt)]
	# remove zeros
	lowbound = np.mean(heatmap[heatmap>0])
	heatmap[heatmap<lowbound] = np.NaN
	# draw heatmap on top of image
	ax.imshow(heatmap, cmap='jet', alpha=alpha)

	# FINISH PLOT
	# invert the y axis, as (0,0) is top left on a display
	ax.invert_yaxis()
	# save the figure if a file name was provided
	if savefilename != None:
		fig.savefig(savefilename)
	
	return fig

# adapted from PyGaze
def draw_display(dispsize, imagefile=None):
	"""Returns a matplotlib.pyplot Figure and its axes, with a size of
	dispsize, a black background colour, and optionally with an image drawn
	onto it

	arguments

	dispsize		-	tuple or list indicating the size of the display,
					e.g. (1024,768)

	keyword arguments

	imagefile		-	full path to an image file over which the heatmap
					is to be laid, or None for no image; NOTE: the image
					may be smaller than the display size, the function
					assumes that the image was presented at the centre of
					the display (default = None)

	returns
	fig, ax		-	matplotlib.pyplot Figure and its axes: field of zeros
					with a size of dispsize, and an image drawn onto it
					if an imagefile was passed
	"""

	# construct screen (black background)
	screen = np.zeros((dispsize[1], dispsize[0], 3), dtype='float32')
	# if an image location has been passed, draw the image
	if imagefile != None:
		# check if the path to the image exists
		if not os.path.isfile(imagefile):
			raise Exception("ERROR in draw_display: imagefile not found at '%s'" % imagefile)
		# load image
		img = image.imread(imagefile)

		# width and height of the image
		w, h = len(img[0]), len(img)
		# x and y position of the image on the display
		x = dispsize[0] / 2 - w / 2
		y = dispsize[1] / 2 - h / 2
		# draw the image on the screen
		screen[y:y + h, x:x + w, :] += img
	# dots per inch
	dpi = 100.0
	# determine the figure size in inches
	figsize = (dispsize[0] / dpi, dispsize[1] / dpi)
	# create a figure
	fig = plt.figure(figsize=figsize, dpi=dpi, frameon=False)
	ax = plt.Axes(fig, [0, 0, 1, 1])
	ax.set_axis_off()
	fig.add_axes(ax)
	# plot display
	ax.axis([0, dispsize[0], 0, dispsize[1]])
	ax.imshow(screen)  # , origin='upper')

	return fig, ax

def run():
	#option 1: input from command line
	# heatmap_from_input()
	
	#option 2: create heatmaps with specified arguments
	draw_heatmap('fixations.csv','gui', 'fixations_duration.png',durationWeight=False)

	# draw_heatmap('fixations.csv','gui', 'fixations_duration.png',durationWeight=True)
	# draw_heatmap('fixations_autonomous.csv','gui', 'fixations_autonomous_duration.png',durationWeight=True)
	# draw_heatmap('fixations_manual.csv','gui', 'fixations_manual_duration.png',durationWeight=True)
	# draw_heatmap('pl_events.csv', 'events', 'pl_events_duration.png', durationWeight=True)

	# draw_heatmap('fixations.csv','gui', 'fixations.png')
	# draw_heatmap('fixations_autonomous.csv', 'gui', 'fixations_autonomous.png')
	# draw_heatmap('fixations_manual.csv', 'gui', 'fixations_manual.png')
	# draw_heatmap('pl_events.csv', 'events', 'pl_events.png')
	# draw_heatmap('pl_samples.csv', 'samples', 'pl_samples.png') 
	# draw_heatmap('pl_cleaned_samples.csv', 'samples', 'pl_cleaned_samples.png')
	
run()