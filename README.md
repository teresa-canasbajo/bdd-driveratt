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

### For pyglui:
##### note that this was added as a submodule inside /lib
`sudo apt-get install libglew-dev
`
`sudo pip3 install git+https://github.com/pupil-labs/pyglui
`
`sudo python3 setup.py install
`
#### Dependencies:
`sudo apt-get install cmake libx11-dev xorg-dev libglu1-mesa-dev freeglut3-dev libglew1.5 libglew1.5-dev libglu1-mesa libglu1-mesa-dev libgl1-mesa-glx libgl1-mesa-dev`

### For ceres:
##### note that this was added as a submodule inside /lib
##### it needs submodule eigen. clone it in lib as 'eigen3'

`cd 'pathtoceressubmoduleinlib' && \
		mkdir -p build && cd build && \
		mkdir -p ../../build_ceres && \
		cmake .. -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX='../build_ceres' -DEIGEN_INCLUDE_DIR_HINTS='../../eigen3' -DEIGEN_INCLUDE_DIR='../../eigen3' && \
		make install`