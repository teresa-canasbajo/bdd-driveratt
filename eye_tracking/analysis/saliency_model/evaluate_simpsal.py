import matlab.engine # only supports python 2.7, 3.3, 3.4
import numpy as np
import skimage.io as skio 
import os
import glob

if not os.path.exists('simpsal_maps'):
	os.makedirs('simpsal_maps')

eng = matlab.engine.start_matlab()
eng.addpath('./simpsal/')

to_process = glob.glob('frames/*')

# fixations = utils.get_fixations_data()
fixations = [(random.uniform(0, 1), random.uniform(0, 1)) for _ in to_process]
n = len(to_process)

for i in range(n):
	image_path = to_process[i]
	im = eng.imread(image_path)
	eng.workspace['im'] = im
	base_map = eng.eval('simpsal(im, default_fast_param)')
	eng.workspace['map'] = base_map
	saliency_map = np.array(eng.eval('mat2gray(map)'))
	saliency_map_big = np.array(eng.eval('mat2gray(imresize(map, [ size(im, 1), size(im, 2) ] ))'))
	skio.imsave('simpsal_maps/' + image_path[6:-3] + 'png', saliency_map)
	skio.imsave('simpsal_maps/' + image_path[6:-4] + '_big.png', saliency_map_big)

	h, w = saliency_map_big.shape
	fixation_w = fixations[i][0]*w
	fixation_h = fixations[i][1]*h

	percentage_fixations_explained += (1-saliency_map[fixation_h][fixation_w])

print("Percentage of fixations explained by saliency (AWS): %f" % percentage_fixations_explained/len(fixations))