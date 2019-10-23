# bdd-driveratt
Project in collaboration with Berkeley Deep Drive on driver's attention in manual, semi-autonomous and autonomous vehicles. It uses Pupil Labs and a driving simulator.

The main goal of this code is to allow for collection and analysis of eye movement data from Pupil Labs glasses avoiding the use of their GUI.

Heavily based on behinger/etcomp repository (https://github.com/behinger/etcomp). We deeply appreciate the great code they put together.

This project includes:
- Matlab and Python scripts to record eye movement data using Pupil Labs glasses.
- Preprocessing pipeline for Pupil Labs glasses.
- Makefile for all requirements.


# Instructions
1. Clone project and intialize submodules

`git clone https://github.com/tere93/bdd-driveratt`

`git submodule update --init`

2. Run Make file: generates a virtual environment (bdddriverattenv), runs requirements.pip with all required python packages and requirements for Pupil Labs.

`make
`

3. You will still need to install the following packages with sudo/root privileges:

`pkg-config
`

`automake`

`cmake`

`python3-dev
`

`libglew-dev
`

`xorg-dev libglu1-mesa-dev` <-- needed for libglew

`libportaudio2` <-- for pyaudio

`portaudio19-dev` <-- for pyaudio

`pyaudio`

# To do:
- Add simulator environment scenarios (coded on Prescan/simulink) for driving experiments.
- Add analysis to categorize eye movements.


