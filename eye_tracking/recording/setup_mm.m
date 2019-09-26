%==========================================================================
% Setup the middleman computer to recognize the pupil eyetracker
%==========================================================================

clear 
close

%% set python path and start server
setenv('PATH', '/Library/Frameworks/Python.framework/Versions/3.6/bin:/Library/Frameworks/Python.framework/Versions/3.6/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin')
system('python3 /Users/tombullock/Documents/Psychology/Pupil_Labs/mtaung_scripts/sample_mm.py &')
pause(1)

%% pupil link UDP setup
hUDP = udp('127.0.0.1',8008,'Timeout',0.5);
pause(1)
fopen(hUDP);
pause(1)
