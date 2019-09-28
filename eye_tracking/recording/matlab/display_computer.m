%==========================================================================
% Setup the middleman computer to recognize the pupil eyetracker
%==========================================================================

clear 
close

%% set python path and start server
setenv('PATH', '/usr/bin/python')
system('python3 /home/whitney/Teresa/bdd-driveratt/eye_tracking/recording/pupil_mm/sample_mm.py &')
pause(1)

%% pupil link UDP setup
hUDP = udp('192.168.0.113', 8008,'Timeout',0.5);
pause(1)
fopen(hUDP);
pause(1)

%% start/stop calibration (press esc. to quit) 
fwrite(hUDP,'START_CAL')
// fwrite(hUDP,'STOP_CAL')

%% start recording 
SjNum = 999; 
SjSession = 1;
SjCondition = 1;
ExpID = 'ab';
% send this command to start the recording and set a custom name for the
% directory. Note that START_REC must be present and followed by a space in
% order for the recording to start ('START_REC XXX').  You can do what you 
% want with regards to customizing the file name, fields etc.
// fwrite(hUDP,sprintf('START_REC sj%d_se%02d_cd%02d_%s',SjNum,SjSession,SjCondition,ExpID))
fwrite(hUDP, 'START_REC')
pause(1);   % include pause so first events don't get sent before recording starts

%% send an event code/trigger
fwrite(hUDP,'2') % e.g. send trigger value '2'.  Note that the values you 

%% stop recording
// fwrite(hUDP,'STOP_REC')
pause(1)

%% close hUDP link and clear object
fclose(hUDP);
clear
