% example of running on command line: 
% matlab -nodisplay -nosplash -nodesktop -r "run('/home/jszou/cs/eye_tracking/bdd-driveratt/eye_tracking/analysis/saliency_model/run_aws.m'); exit;"
%
% mkdir aws_maps
mkdir '/media/whitney/New Volume/Teresa/bdd-driveratt/demo/aws_maps'
addpath('./aws/')
% to_process = dir('frames')
to_process = dir('/media/whitney/New Volume/Teresa/bdd-driveratt/demo/frames')
for n=3:length(to_process)
	filename = to_process(n).name
	% im = imread(strcat('frames/', filename))
	im = imread(strcat('/media/whitney/New Volume/Teresa/bdd-driveratt/demo/frames/', filename))
	smap = aws(im)
	graymap = mat2gray(smap)
	% imwrite(graymap, strcat('aws_maps/', filename(1:length(filename)-3)), 'png')
	imwrite(graymap, strcat('/media/whitney/New Volume/Teresa/bdd-driveratt/demo/aws_maps/', filename(1:length(filename)-3)), 'png')
end