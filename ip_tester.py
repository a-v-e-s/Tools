"""
ip_tester.py

Functions return True if input is a valid ip address,
False if not.
"""

import socket
from sys import exc_info


def ip4(n):
    try:
        socket.inet_pton(socket.AF_INET, n)
        return True
    except socket.error:
        return False
    except ValueError:
        print(exc_info())
        print(n, 'was not able to be examined')
        return False


def ip6(n):
    try:
        socket.inet_pton(socket.AF_INET6, n)
        return True
    except socket.error:
        return False
    except ValueError:
        print(exc_info())
        print(n, 'was not able to be examined')
        return False
