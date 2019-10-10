#!/usr/bin/env python3

import socket, pickle
import ip_tester

def name_attackers():
    bad_hosts = []
    unknown_hosts = []
    rules = open('/etc/iptables/rules.v4', 'r')

    print('Working...')

    for x in rules.readlines():
        for y in x.split():
            if ip_tester.ip4(y[:-3]):
                try:
                    bad_hosts.append(socket.gethostbyaddr(y[:-3])[0])
                except socket.herror:
                    unknown_hosts.append(y[:-3])

    with open('bad_hosts.pkl', 'wb') as file:
        pickle.dump(bad_hosts, file)

    print('Bad hosts discovered:')
    for x in bad_hosts:
        print(x)
    print('Unknown hosts:')
    for x in unknown_hosts:
        print(x)
    print('# of Bad hosts discovered:', len(bad_hosts))
    print('# of Unknown hosts:', len(unknown_hosts))


def name_visitors():
    visiting_hosts = []
    unknown_visitors = []
    with open('/home/rock64/Repos/personal_website/guestbook.pkl', 'rb') as file:
        visitors = pickle.load(file)

    print('Working...')

    for x in visitors:
        try:
            visiting_hosts.append(socket.gethostbyaddr(x)[0])
        except socket.herror:
            unknown_visitors.append(x)

    with open('visiting_hosts.pkl', 'wb') as file:
        pickle.dump(visiting_hosts, file)

    print('Visiting hosts:')
    for x in visiting_hosts:
        print(x)
    print('Number of unknown visitors:', len(unknown_visitors))


if __name__ == '__main__':
    name_attakers()
    name_visitors()
