

installfolder = local
VENV = ${installfolder}/bdddriverattvenv

#export VIRTUAL_ENV := $(abspath ${VENV})
#export PATH := ${VIRTUAL_ENV}/bin:${PATH}


install: git-reqs ${VENV} python-reqs compile-dependencies printexport
		echo 'installation done, whew.. you should be very happy that this worked ;)'

git-reqs:
	git submodule update --init

${VENV}:
	virtualenv -p python3 --system-site-packages ${VENV}
	#python3 -m venv --system-site-packages ${VENV}#


python-reqs: ${VENV}
	( \
	. ${VENV}/bin/activate; \
	pip3 install --upgrade -r requirements.pip;\
	pip3 install setuptools -U --force;\
	pip3 install git+https://github.com/has2k1/plotnine.git;\
	)


compile-dependencies: glfw glog ceres
		echo 'done'

uneyesrc = ${installfolder}/build/src_uneye

uneye: ${VENV} 
	(\
	. ${VENV}/bin/activate; \
	git clone https://github.com/berenslab/uneye ${uneyesrc};\
	cd ${uneyesrc};\
	pip3 install ./ -r ./requirements.txt\
	)
	
	git pull https://github.com/berenslab/uneye


printexport:
		echo 'use this command before starting python/spyder'
		echo 'export LD_LIBRARY_PATH=${CURDIR}/${ffmpegbuild}/lib/:${CURDIR}/${glfwbuild}/lib/:${CURRDIR}/${ceresbuild}/lib:$$LD_LIBRARY_PATH'

glfwsrc = ${installfolder}/build/src_glfw
glfwbuild = ${installfolder}/build/build_glfw
glfw: ${glfwsrc} ${glfwbuild}
		echo 'done'

${glfwsrc}:
		git clone https://github.com/glfw/glfw ${glfwsrc}

${glfwbuild}:
		mkdir ${glfwsrc}/build
		cd ${glfwsrc}/build && \
		cmake -DCMAKE_INSTALL_PREFIX='../../build_glfw' -DBUILD_SHARED_LIBS=ON ../ &&\
		make -j && \
		make install

#### uncomment maybe:
# pyavsrc = ${installfolder}/build/src_pyav
#
# ${pyavsrc}:
# 		git clone git@github.com:PyAV-Org/PyAV ${pyavsrc}
#
# pyav: ${VENV} ${pyavsrc} ffmpeg
# 		cd ${pyavsrc} && \
#         ./scripts/build-deps && \
#         make
#### until here

# pygluisrc = ${installfolder}/build/src_pyglui

#${pygluisrc}:
		#git clone http://github.com/pupil-labs/pyglui --recursive ${pygluisrc}

# git checkout setup.py && \
#
# pyglui: ${VENV} ${pygluisrc}
# 		cd ${pygluisrc} && \
# 		sudo python3 setup.py install


#### opencv uncommented 0724
# opencvsrc = ${installfolder}/build/src_opencv
# opencvbuild = ${installfolder}/build/build_opencv
# ${opencvsrc}:
# 			git clone https://github.com/itseez/opencv ${opencvsrc}
# 			cd ${opencvsrc} &&\
# 			git checkout b38c50b
#
#
#
#
# opencv: ${opencvbuild}
# 	echo 'opencv done'
#
# ${opencvbuild}: ${opencvsrc}
# 		mkdir -p ${opencvbuild}
# 		mkdir -p ${opencvsrc}/build
# 	        cd ${opencvsrc}/build && \
#                 cmake -D CMAKE_BUILD_TYPE=RELEASE -D BUILD_TBB=ON -D WITH_TBB=ON -D WITH_CUDA=OFF -D BUILD_opencv_python2=OFF -DBUILD_opencv_python3=ON  -D CMAKE_INSTALL_PREFIX='../../build_opencv' ../ && \
#                 make -j4 && \
#                 make install
# 		# now add opencv to python
# 		echo 'set up for python 3.6, you may need to adjust for your python version'
# 		cp ${opencvbuild}/lib/python3.7/site-packages/cv2.cpython-37m-x86_64-linux-gnu.so ${VENV}/lib/python3.7/site-packages/cv2.cpython-37m-x86_64-linux-gnu.so
# cleanopencv:
# 		rm -r ${opencvbuild}
# 		rm -r ${opencvsrc}/build
##### until here opencv uncommented 0724

ffmpegsrc = ${installfolder}/build/src_ffmpeg
ffmpegbuild = ${installfolder}/build/build_ffmpeg

yasmsrc =  ${installfolder}/build/src_yasm/
yasmbuild = ${installfolder}/build/build_yasm/

ceressrc = ${installfolder}/build/src_ceres/
ceresbuild = ${installfolder}/build/build_ceres/
eigensrc = ${installfolder}/build/eigen3/

${ceressrc}:
		git clone https://ceres-solver.googlesource.com/ceres-solver ${ceressrc}
		cd ${ceressrc}&&\
		git checkout 2496500436da3b72ac4431e7878d5d5197e2031b
${eigensrc}:
		git clone https://github.com/eigenteam/eigen-git-mirror.git ${eigensrc}
		cd ${eigensrc}&&\
		git checkout tags/3.3.4

glogsrc = ${installfolder}/build/src_glog
glogbuild = ${installfolder}/build/build_glog
glog: ${glogbuild}
		echo 'done'

${glogsrc}:
		git clone https://github.com/google/glog ${glogsrc}

${glogbuild}: ${glogsrc}
		echo 'here'
# 		mkdir ${glogsrc}
# 		git clone https://github.com/google/glog ${glogsrc}
		echo ${glogsrc}
		pwd
		cd ${glogsrc} && pwd && export CXXFLAGS="-fPIC" && cmake . && make VERBOSE=1
# 		make install



#suitesparsesrc   = ${installfolder}/build/src_suitesparse
#suitesparsebuild = ${installfolder}/build/build_suitesparse

#${suitesparsesrc}: #

#		git clone https://github.com/jlblancoc/suitesparse-metis-for-windows/ ${suitesparsesrc}


#${suitesparsebuild}: ${suitesparsesrc}
#		cd ${suitesparsesrc} &&\
#		mkdir -p build &&\
#		cd build && \
#		cmake ../ -DCMAKE_INSTALL_PREFIX='../../build_suitesparse' &&\
#		make install
		

ceres : ${ceresbuild}
	echo 'done'
${ceresbuild}:  ${ceressrc} ${eigensrc}

		mkdir ${installfolder}/build/build_ceres &&\
		cd ${ceressrc} &&\
		cmake . -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX='../build_ceres' -DEIGEN_INCLUDE_DIR_HINTS='../eigen3' -DEIGEN_INCLUDE_DIR='../eigen3' &&\
		make install
		#sudo sh -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/ceres.conf'
		#sudo ldconfig
# 		mkdir -p build && cd build && \
# 		mkdir -p ../../build_ceres && \
${ffmpegsrc}:
		wget http://launchpad.net/ubuntu/+archive/primary/+files/ffmpeg_3.3.4.orig.tar.xz &&\
		mkdir ${ffmpegsrc}
		tar -xf ffmpeg_3.3.4.orig.tar.xz ffmpeg-3.3.4
		mv ffmpeg-3.3.4/* ${ffmpegsrc}
		rm -r ffmpeg-3.3.4
		rm ffmpeg_3.3.4.orig.tar.xz

ffmpeg: ${ffmpegbuild}
		echo 'installed ffmpeg'

${ffmpegbuild}: ${yasmbuild} ${ffmpegsrc}
		export PATH=${PATH}:${CURDIR}/${yasmbuild}/bin && \
		cd ${ffmpegsrc} && \
		./configure --prefix='../build_ffmpeg' --enable-shared --enable-pic --cc="gcc -m64 -fPIC" --extra-cflags="-fPIC" && \
		make -j4 && \
		make install

cleanffmpeg:
		rm -r ${ffmpegsrc}
		rm -r ${ffmpegbuild}

${yasmsrc}:
		git clone https://github.com/yasm/yasm ${yasmsrc}

yasm: ${yasmbuild}
	echo 'installed yasm'

nodejsbuild = $(PWD)/${installfolder}/build/build_nodejs

nodejs: ${nodejsbuild}
	echo 'installed nodejs'


${nodejsbuild}:
		echo $(PWD) 
		curl -L https://git.io/n-install | N_PREFIiX=${nodejsbuild} bash -s -- -y		

jupytertoc: ${nodejsbuild}
	        (\
		. ${VENV}/bin/activate; \
                export PATH='$(PATH):${nodejsbuild}/bin'; \
		jupyter labextension install @jupyterlab/toc;\
		)

${yasmbuild}: ${yasmsrc}
		cd ${yasmsrc} && \
		./autogen.sh && \
		./configure --prefix=${CURDIR}/${yasmbuild} && \
		make yasm && \
		make install

cleanyasm:
		rm -r ${yasmsrc}
		rm -r ${installfolder}/build/build_yasm

path: compile-dependencies python-reqs ${VENV}
		export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${ffmpegbuild}
