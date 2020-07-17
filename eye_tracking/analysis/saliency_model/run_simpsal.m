% Convenience script for running pre-packaged IttiKoch2 algorithm on all .png files in a specified input directory
% and saving all B/W result images to the specified output directory. Paths should be modified as needed.
%
% example of running on command line: 
% matlab -nodisplay -nosplash -nodesktop -r "run('/home/whitney/Teresa/bdd-driveratt/eye_tracking/analysis/saliency_model/run_simpsal.m'); exit;"

mkdir '/media/whitney/New Volume/Teresa/bdd-driveratt/demo/simpsal_maps' % modify as needed
addpath('./simpsal/')
to_process = dir('/media/whitney/New Volume/Teresa/bdd-driveratt/demo/frames') % modify as needed
parfor n=3:length(to_process)
	filename = to_process(n).name
	im = imread(strcat('/media/whitney/New Volume/Teresa/bdd-driveratt/demo/frames/', filename)) % modify as needed
	smap = simpsal(im, default_fast_param)
	graymap = mat2gray(smap)
	graymap_big = imresize(graymap, [ size(im, 1), size(im, 2) ] )
	imwrite(graymap, strcat('/media/whitney/New Volume/Teresa/bdd-driveratt/demo/simpsal_maps/', filename(1:length(filename)-3), 'png')) % modifiy as needed
	imwrite(graymap, strcat('/media/whitney/New Volume/Teresa/bdd-driveratt/demo/simpsal_maps/', filename(1:length(filename)-4), '_big.png')) % modify as needed
end