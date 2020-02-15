"""
monitor.py is a script to monitor traffic to my web server and generate
a report on it
"""

import pickle, re, sys
import ip_tester


def signin(logfile):
    try:
        with open('/home/rock64/personal_website/guestbook.pkl', 'rb') as guestbook:
            guests = pickle.load(guestbook)
    except EOFError:
        if input('\nGuestbook empty. Should we start fresh? [y/n]\n').lower() == 'y':
            guests = []
        else:
            sys.exit()
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

    with open('/home/rock64/Repos/personal_website/num', 'w') as num:
        num.write(str(len(guests)))

    with open('../personal_website/guestbook.pkl', 'wb') as guestbook:
        pickle.dump(guests, guestbook)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for x in sys.argv[1:]:
            print('Checking ', x, ' for new visitors!', sep='')
            signin(x)
    else:
        signin('/var/log/apache2/access.log')
