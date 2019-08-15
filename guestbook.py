"""
monitor.py is a script to monitor traffic to my web server and generate
a report on it
"""

import pickle, re, sys
import ip_tester


def signin(logfile):
    try:
        with open('guestbook.pkl', 'rb') as guestbook:
            guests = pickle.load(guestbook)
    except EOFError:
        print('\nGuestbook empty. We will start fresh.\n')
        guests = []
    except FileNotFoundError:
        print('\nNo guestbook found. We will create a new one.\n')
        guests = []

    log = open(logfile, 'r')
    for x in log.readlines():
        if re.search(r'\s404\s', x):
            continue
        else:
            for y in x.split(' '):
                if ip_tester.ip4(y):
                    if y in guests:
                        break
                    else:
                        guests.append(y)
                elif ip_tester.ip6(y):
                    if y in guests:
                        break
                    else:
                        guests.append(y)

    with open('guestbook.pkl', 'wb') as guestbook:
        pickle.dump(guests, guestbook)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for x in sys.argv[1:]:
            print('Checking ', x, ' for new visitors!', sep='')
            signin(x)
    else:
        signin('/var/log/apache2/access.log')
