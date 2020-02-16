# bdd-driveratt
Project in collaboration with Berkeley Deep Drive on driver's attention in manual, semi-autonomous and autonomous vehicles. It uses Pupil Labs and a driving simulator.

The main goal of this code is to allow for collection and analysis of eye movement data from Pupil Labs glasses using their API.

Heavily based on behinger/etcomp repository (https://github.com/behinger/etcomp). We deeply appreciate the great code they put together. The main difference with this code is that we use the Pupil Labs API versions >=1.17.

This project includes:
- Makefile for all requirements (in progress!).
- Recording: Matlab and Python scripts to record eye movement data using Pupil Labs glasses.
- Preprocessing: Preprocessing pipeline for Pupil Labs glasses.
- Eyetracking_analysis: 
	- Analysis code for categorization of eye movements during driving. Based on Tensorflow 		models.
	- Analysis code for comparison of gaze distributions of different conditions in driving.

Teresa Canas-Bajo

## Instructions for Use of Eye-tracking Code

1. Go to the relevant folder (recording, preprocessing or analysis) and follow the instructions there.
2. The folder lib has three submodules needed for this code: 

- pupil_API: Pupil labs API, under 'pupil_API': https://github.com/pupil-labs/pupil
- Pyuvc: Python bindings for the Pupil Labs fork of libuvc with super fast jpeg decompression using libjpegturbo (utilizing the tubojpeg api): https://github.com/pupil-labs/pyuvc
- nslr_hmm: Python implementation of the NSLR-HMM eye movement identification algorithm: https://github.com/pupil-labs/nslr-hmm

## To do:
- Add simulator environment scenarios (coded on Prescan/simulink) for driving experiments.
- Finalize makefile
- Fix surface detector and implement to preprocessing pipeline


