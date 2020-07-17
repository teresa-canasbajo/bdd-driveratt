% Convenience script for running pre-packaged AWS algorithm on all .png files in a specified input directory
% and saving all B/W result images to the specified output directory. Paths should be modified as needed.
%
% example of running on command line: 
% matlab -nodisplay -nosplash -nodesktop -r "run('/home/whitney/Teresa/bdd-driveratt/eye_tracking/analysis/saliency_model/run_aws.m'); exit;"

mkdir '/media/whitney/New Volume/Teresa/bdd-driveratt/paths/aws_maps_C' % modify as needed
addpath('./aws/')
to_process = dir('/media/whitney/New Volume/Teresa/bdd-driveratt/paths/frames_C') % modify as needed
parfor (n=3:length(to_process), 4)
	filename = to_process(n).name
	im = imread(strcat('/media/whitney/New Volume/Teresa/bdd-driveratt/paths/frames_C/', filename)) % modify as needed
	smap = aws(im)
	graymap = mat2gray(smap)
	imwrite(graymap, strcat('/media/whitney/New Volume/Teresa/bdd-driveratt/paths/aws_maps_C/', filename(1:length(filename)-3), 'png')) % modify as needed
end