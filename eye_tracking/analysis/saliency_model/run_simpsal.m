% mkdir simpsal_maps
mkdir '/media/whitney/New Volume/Teresa/bdd-driveratt/demo/simpsal_maps'
addpath('./simpsal/')
% to_process = dir('frames')
to_process = dir('/media/whitney/New Volume/Teresa/bdd-driveratt/demo/frames')
for n=3:length(to_process)
	filename = to_process(n).name
	% im = imread(strcat('frames/', filename))
	im = imread(strcat('/media/whitney/New Volume/Teresa/bdd-driveratt/demo/frames/', filename))
	smap = simpsal(im, default_fast_param)
	graymap = mat2gray(smap)
	graymap_big = imresize(graymap, [ size(im, 1), size(im, 2) ] )
	% imwrite(graymap, strcat('simpsal_maps/', filename(1:length(filename)-3)), 'png')
	% imwrite(graymap, strcat('simpsal_maps/', filename(1:length(filename)-4)), '_big.png')
	imwrite(graymap, strcat('/media/whitney/New Volume/Teresa/bdd-driveratt/demo/simpsal_maps/', filename(1:length(filename)-3)), 'png')
	imwrite(graymap, strcat('/media/whitney/New Volume/Teresa/bdd-driveratt/demo/simpsal_maps/', filename(1:length(filename)-4)), '_big.png')
end