#! /bin/sh - 

sudo service ntp stop
sleep 10
sudo ntpdate 98.152.165.38
sleep 20

valid=true

while [ $valid ]
do
echo $(date +"%H:%M:%S:%3N")



done
