#!/usr/local/bin/python3

import os, sys, random, subprocess

if os.getuid() != 0:
	print('Try again as root!')
	sys.exit()

os.popen('sudo ifconfig eth0 192.168.1.4')
os.popen('sudo noip2')
os.popen('sudo mount -t ext4 /dev/mmcblk1p1 /srv/ftp')

if input('\nStart ssh server? [y/n]\n').lower() == 'y':
	os.popen('sudo systemctl start ssh')

if '/usr/lib/xorg/Xorg' in subprocess.getoutput('ps -aux | grep Xorg'):
	background = os.path.join('/home/rock64/Pictures/backgrounds', random.choice(os.listdir('/home/rock64/Pictures/backgrounds')))
	command = 'feh --bg-fill ' + background
	os.popen(command)
	

if input('\nStart nfs server? [y/n]\n').lower() == 'y':
	print('\nSyncing home directory with nfs directory...\n')
	os.chdir('/home/rock64')
	os.popen('sudo rsync -aAv --delete --exclude=.cache /home/rock64 /srv/nfs')
	print('\nDone syncing...\n')
	os.popen('sudo systemctl start nfs-kernel-server')
	
print('Done!')
