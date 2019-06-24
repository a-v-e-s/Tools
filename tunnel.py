#!/usr/local/bin/python3

import os, sys

def tunnel(protocol):
	os.chdir('/home/crowbar/CyberGhost/us-' + protocol)
	try:
		os.popen('sudo openvpn openvpn.ovpn')
	except Exception:
		print('\nFailed to start vpn.\n')
		print(sys.exc_info())


if __name__ == '__main__':
    tunnel('udp')