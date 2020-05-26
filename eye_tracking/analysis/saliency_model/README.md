# Overview

This module contains code for using saliency models to predict saliency maps for our driving simulation videos. As different models
are coded differently, the structure of the code varies a bit.

# Setup

Ensure that you have a working version of MATLAB installed and that the MATLAB Engine API for Python is configured. For information on how to do
that, please refer here https://www.mathworks.com/help/matlab/matlab_external/get-started-with-matlab-engine-for-python.html. Note that the engine is 
only compatible with Python versions 2.7, 3.3, and 3.4. 

# AWS and IttiKoch2

`run_aws.m` and `run_simpsal.m` provide convenience scripts for running the licensed AWS/IttiKoch2 code on all images in a specified directory. An example command line call is shown below. Ensure that the input and output directory paths in the script are configured correctly for your local environment before running.
```
matlab -nodisplay -nosplash -nodesktop -r "run('FULL_PATH_TO_RUNFILE'); exit;"
```
