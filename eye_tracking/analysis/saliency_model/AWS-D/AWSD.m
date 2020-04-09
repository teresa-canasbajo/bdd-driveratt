%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%             DYNAMIC WHITENING SALIENCY (AWS-D) MODEL               %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% This function computes a dynamic saliency map from a video. 
%
%   
% Usage:
%     OutSaliencyMovie = AWSD ('SCE_Bur_1.avi');
%
% Input: An video avi
%
% Returned values:
%    OutSaliencyMovie         - Saliency map of the input video.
%  
%
%   %%%%%%%%%%%%%%NOTE: you must be patient, the algorithm is very slow!!

%   Research Team: 
%       Victor Leboran Alvarez. Predoctoral Student at the Santiago de Compostela University (CITIUS).
%       Xose Manuel Pardo Lopez. Associate Professor. University of Santiago de Compostela (Spain).
%       Xose R. Fernandez Vidal. Associate Professor. Santiago de Compostela University (Spain).
%       Anton Garcia Diaz. AIMEN Technology Center - O Porrinho, Spain.
%
% References:
%
% The model is described in:
%
% 1- V. Leboran and A. Garcia-Diaz and X. Fdez-Vidal and X. Pardo
% Dynamic Whitening Saliency. In
% IEEE Transactions on Pattern Analysis and Machine Intelligence,
% Accepted May 2016.   
%
%2.-V. Leboran, A. Garcia-Diaz, X.R. Fdez-Vidal,  X.M. Pardo , 
%  Dynamic Saliency from Adaptative Whitening. 
%  5th International Work-Conference on the Interplay Between Natural 
%  and Artificial Computation, Mallorca (Spain), 
%  Springer Berlin Heidelberg, pp. 345-354 , 2013.
%
% Copyright (c), (Last update) May 2016,  Victor Leboran et al.
% CITIUS,
% The University of Santiago de Compostela
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
% 
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
% 
% You should have received a copy of the GNU General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>.

