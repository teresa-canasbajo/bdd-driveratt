import matlab.engine # only supports python 2.7, 3.3, 3.4
import numpy as np
import skimage.io as skio 
import os
import glob
import utils

if not os.path.exists('aws_d_videos'):
	os.makedirs('aws_d_videos')

eng = matlab.engine.start_matlab()
eng.addpath('./AWS-D/')

to_process = glob.glob('videos/*')

# fixations = utils.get_fixations_data()
fixations = [(random.uniform(0, 1), random.uniform(0, 1)) for _ in to_process]

percentage_fixations_explained = 0
n = len(to_process)

for i in range(n):
	image_path = to_process[i]
	im = eng.imread(image_path)
	saliency_map = eng.aws(im)
	saliency_map = np.array(saliency_map)
	saliency_map -= np.min(saliency_map)
	saliency_map /= np.max(saliency_map)
	skio.imsave('aws_d_videos/' + image_path[6:-3] + 'png', saliency_map)

	h, w = saliency_map.shape
	fixation_w = fixations[i][0]*w
	fixation_h = fixations[i][1]*h

	percentage_fixations_explained += (1-saliency_map[fixation_h][fixation_w])


print("Percentage of fixations explained by saliency (AWS): %f" % percentage_fixations_explained/len(fixations))