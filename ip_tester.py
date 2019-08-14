"""
ip_tester.py

Functions return True if input is a valid ip address,
False if not.
"""

import socket


def ip4(n):
	try:
		socket.inet_pton(socket.AF_INET, n)
		return True
	except socket.error:
		return False

		
def ip6(n):
	try:
		socket.inet_pton(socket.AF_INET6, n)
		return True
	except socket.error:
		return False
