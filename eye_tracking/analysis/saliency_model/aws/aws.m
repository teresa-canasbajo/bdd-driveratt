%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%             ADAPTATIVE WHITENING SALIENCY MODEL (AWS)               %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% This function computes a saliency map from an image. 
%
%   
% Usage:
%     im = imread('andaina.jpg');
%     SaliencyMap = aws(im);
%      or
%     SaliencyMap = aws(im,fr,sp);
% or:
%     SaliencyMap = aws('andaina.jpg');
%       or
%     SaliencyMap = aws('andaina.jpg',fr,sp);
%
% Input values:
% fr: control parameter of resize input image. It take values in interval (0,1] (default 1).
% sp - control parameter of smooth gaussian  (default 2.1). If sp=0 --> without gaussian smooth.  
%      The gaussian sigma is obtained by sigma= max(rows,cols) * sp * 0.01;
%
% Apart from the image, all parameters have defaults assigned by authors
%
% Returned values:
%    SaliencyMap         - Saliency map of the input image.
%   
% References:
% 1.- Garcia-Diaz, A.; Fdez-Vidal, X. R; Pardo, X. M and Dosil, R.. 
%     Saliency from hierarchical adaptation through decorrelation and variance normalization. 
%     In Image and Vision Computing, 30 (1): 51-64, 2012.
%
% 2.- Garcia-Diaz, A.; Leboran, V.; Fdez-Vidal, X. R. and Pardo, X. M.. 
%     On the relationship between optical variability, visual saliency, and eye fixations: 
%      A computational approach. In Journal of Vision, 12 (6), 2012.
%
% 3. A Garcia-Diaz, XR Fdez-Vidal, XM Pardo and R Dosil, Saliency Based on
%    Decorrelation and Distinctiveness of Local Responses, LNCS 5702, CAIP
%    2009  
% 4. A Garcia-Diaz, XR Fdez-Vidal, XM Pardo and R Dosil, Decorrelation and
%    Distinctiveness Provide with Human-Like Saliency, LNCS 5807, ACIVS
%    2009 
%
% Copyright (c), Computer Vision Group
% CITiUS
% The University of Santiago de Compostela
% Galiza
%
% Permission is hereby  granted, free of charge, to any  person obtaining a
% copy of this software and associated documentation files (the
% "Software"), to deal in the Software without restriction, subject to the
% following conditions: 
%
% The above copyright notice and this permission notice shall be included
% in all copies or substantial portions of the Software. 
%
% The software is provided "as is", without warranty of any kind.