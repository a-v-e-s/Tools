#!/usr/local/bin/python3

import os, sys, random, subprocess, threading
from pull import pull
from tunnel import tunnel

if os.getuid() != 0:
	print('Try again as root!')
	sys.exit()


def start_blacktop():
	os.popen('sudo rfkill block bluetooth')
	if input('\nAirplane mode? [y/n]\n').lower() == 'y':
		os.popen('sudo rfkill block wifi')
	
	vpn = input('\nStart VPN?\nEnter type: [udp/tcp]\n').lower()
	if vpn == 'udp' or 'tcp':
		threading.Thread(None, tunnel, args=(vpn,)).run()
	"""
	for x in os.listdir('/home/crowbar/Repos'):
		threading.Thread(None, pull, args=(os.path.join('/home/crowbar/Repos', x), x)).run()
	"""


def start_rock64():
	os.popen('sudo noip2')
	os.popen('sudo mount -t ext4 /dev/mmcblk1p1 /srv/ftp')

	if input('\nStart ssh server? [y/n]\n').lower() == 'y':
		os.popen('sudo systemctl start ssh')

	if '/usr/lib/xorg/Xorg' in subprocess.getoutput('ps -aux | grep Xorg'):
		background = os.path.join('/home/rock64/Pictures/backgrounds', random.choice(os.listdir('/home/rock64/Pictures/backgrounds')))
		command = 'feh --bg-fill ' + background
		os.popen(command)


	if input('\nStart nfs server for home directory? [y/n]\n').lower() == 'y':
		os.popen('sudo systemctl start nfs-kernel-server')
	"""
	for x in os.listdir('/home/rock64/Repos'):
		threading.Thread(None, pull, args=(os.path.join('/home/rock64/Repos', x), x)).run()
	"""
	print('Done!')


with open('/etc/hostname', 'r') as host:
	name = host.readline()
	if 'blacktop' in name:
		start_blacktop()
	elif 'rock64' in name:
		start_rock64()