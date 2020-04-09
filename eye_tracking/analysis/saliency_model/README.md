# Overview

This module contains code for using saliency models to predict saliency maps for our driving simulation videos. As different models
are coded differently, the structure of the code varies a bit.

# Setup

## AWS

Ensure that you have a working version of MATLAB installed and that the MATLAB Engine API for Python is configured. For information on how to do
that, please refer here https://www.mathworks.com/help/matlab/matlab_external/get-started-with-matlab-engine-for-python.html. Note that the engine is 
only compatible with Python versions 2.7, 3.3, and 3.4. 

To generate saliency maps, simply run
'''
python run_aws.py
'''
and the maps will be populated in the directory "aws_maps".