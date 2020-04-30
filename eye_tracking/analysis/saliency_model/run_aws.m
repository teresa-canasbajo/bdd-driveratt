% example of running on command line: 
% matlab -nodisplay -nosplash -nodesktop -r "run('/home/whitney/Teresa/bdd-driveratt/eye_tracking/analysis/saliency_model/run_aws.m'); exit;"
%
% mkdir aws_maps
mkdir '/media/whitney/New Volume/Teresa/bdd-driveratt/paths/aws_maps_C'
addpath('./aws/')
% to_process = dir('frames')
to_process = dir('/media/whitney/New Volume/Teresa/bdd-driveratt/paths/frames_C')
parfor (n=3:length(to_process), 4)
	filename = to_process(n).name
	% im = imread(strcat('frames/', filename))
	im = imread(strcat('/media/whitney/New Volume/Teresa/bdd-driveratt/paths/frames_C/', filename))
	smap = aws(im)
	graymap = mat2gray(smap)
	% imwrite(graymap, strcat('aws_maps/', filename(1:length(filename)-3)), 'png')
	imwrite(graymap, strcat('/media/whitney/New Volume/Teresa/bdd-driveratt/paths/aws_maps_C/', filename(1:length(filename)-3), 'png'))
end