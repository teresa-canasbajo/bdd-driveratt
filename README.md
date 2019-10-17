# bdd-driveratt
Project in collaboration with Berkeley Deep Drive on driver's attention in manual, semi-autonomous and autonomous vehicles. It uses Pupil Labs and a driving simulator.

Please install packages listed in Pipfile
We've used pipenv to develop the code

You will still need to install the following packages with sudo/root privileges:
`pkg-config`


## Instructions to install needed packages from root
### For AV:
#### General dependencies
`sudo apt-get install -y python-dev pkg-config
`
#### Library components
`sudo apt-get install -y \
    libavformat-dev libavcodec-dev libavdevice-dev \
    libavutil-dev libswscale-dev libswresample-dev libavfilter-dev`
