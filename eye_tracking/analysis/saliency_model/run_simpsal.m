mkdir simpsal_maps
addpath('./simpsal/')
to_process = dir('frames')
for n=3:length(to_process)
	filename = to_process(n).name
	im = imread(strcat('frames/', filename))
	smap = aws(im)
	graymap = mat2gray(smap)
	graymap_big = imresize(graymap, [ size(im, 1), size(im, 2) ] )
	imwrite(graymap, strcat('simpsal_maps/', filename(1:length(filename)-3)), 'png')
	imwrite(graymap, strcat('simpsal_maps/', filename(1:length(filename)-4)), '_big.png')