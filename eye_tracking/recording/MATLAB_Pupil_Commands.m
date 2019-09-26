%==========================================================================
% Purpose: Enable pupil capture to be controlled with MATLAB and PTB3. 
% Author: Tom Bullock, UCSB Attention Lab
% Date: 02.18.18
% Notes: You must run sample_mm.py to set up the python middle man server
% with pupil_capture before attempting to initialize the UDP connection 
% from MATLAB.
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

%% start/stop calibration (press esc. to quit) 
fwrite(hUDP,'START_CAL')
fwrite(hUDP,'STOP_CAL')

%% start recording 
SjNum = 999; 
SjSession = 1;
SjCondition = 1;
ExpID = 'ab';
% send this command to start the recording and set a custom name for the
% directory. Note that START_REC must be present and followed by a space in
% order for the recording to start ('START_REC XXX').  You can do what you 
% want with regards to customizing the file name, fields etc.
fwrite(hUDP,sprintf('START_REC sj%d_se%02d_cd%02d_%s',SjNum,SjSession,SjCondition,ExpID))
pause(1);   % include pause so first events don't get sent before recording starts

%% send an event code/trigger
fwrite(hUDP,'2') % e.g. send trigger value '2'.  Note that the values you 

%% stop recording
fwrite(hUDP,'STOP_REC')
pause(1)

%% close hUDP link and clear object
fclose(hUDP);
clear