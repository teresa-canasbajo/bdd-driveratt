import sys
import numpy as np
import skimage.io as skio 
import os
import glob
import utils
from scipy import interpolate

if __name__ == "__main__":
	args = sys.argv[1:]
	assert(len(args) >= 1)

	saliency_maps_query = args[0]
	to_process = glob.glob(saliency_maps_query) # modify path as needed

	# fixations = utils.get_fixations_data() 
	fixations = [(np.random.uniform(0, 1), np.random.uniform(0, 1)) for _ in to_process] # comment this line and uncomment above when running with actual fixation data

	percentage_fixations_explained = 0
	n = len(to_process)

	for i in range(n):
		image_path = to_process[i]
		smap = skio.imread(image_path)
		max_value = np.max(smap)

		h, w = smap.shape
		fixation_w = fixations[i][0]*w
		fixation_h = fixations[i][1]*h

		interp = interpolate.RectBivariateSpline(np.arange(h), np.arange(w), smap, kx=1, ky=1) # use linear interpolation to retrieve values for floating point fixations

		percentage_fixations_explained += (max_value-interp(fixation_h, fixation_w, grid=False))/max_value # treats smap value at coord as percentage explainable by saliency
		# percentage_fixations_explained += (1 if (max_value-interp(fixation_h, fixation_w, grid=False))/max_value > 0.8 else 0) # binarizes explainability

	print("Percentage of fixations explained by saliency: %f" % (percentage_fixations_explained/len(fixations)))