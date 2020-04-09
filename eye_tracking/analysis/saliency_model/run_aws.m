mkdir aws_maps
addpath('./aws/')
to_process = dir('frames')
for n=3:length(to_process)
	filename = to_process(n).name
	im = imread(strcat('frames/', filename))
	smap = aws(im)
	graymap = mat2gray(smap)
	imwrite(graymap, strcat('aws_maps/', filename(1:length(filename)-3)), 'png')
end