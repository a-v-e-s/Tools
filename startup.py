import os, sys, random

if os.getuid() != 0:
	print('Try again as root!')
	sys.exit()

os.popen('sudo noip2')
background = os.path.join('/home/rock64/Pictures', random.choice(os.listdir('/home/rock64/Pictures/backgrounds')))
command = 'feh --bg-fill ' + background
os.popen(command)

if input('\nStart ssh server? [y/n]\n').lower() == 'y':
	os.popen('sudo systemctl start ssh')
	
print('Done!')
