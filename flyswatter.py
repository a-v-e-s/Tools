"""
flyswatter.py: utilizes iptables to block ip addresses trying to gain
unauthorized access.

Written by: Jon David Tannehill
"""

import os, sys, re, socket, collections
import ip_tester


class Frog():
    def __init__(self):
        self.known_attackers = []
        self.attackers = []
        rules = open('/etc/iptables/rules.v4', 'r')
        for x in rules:
            if re.search('DROP', x):
                for y in x.split():
                    if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', y):
                        self.known_attackers.append(y[:-3])

    def auth(self, log_):
        failed_attempts = []
        log = open(log_, 'r', encoding='utf8')
        for x in log:
            if re.search('Failed password for', x):
                failed_attempts.append(x)
                continue
            if re.search('Invalid user', x):
                failed_attempts.append(x)
                continue
            if re.search('not allowed because not listed in AllowUsers', x):
                failed_attempts.append(x)
                continue
            if re.search('Did not receive identification string from ', x):
                failed_attempts.append(x)

        suspects = []
        for x in failed_attempts:
            for y in x.split():
                if ip_tester.ip4(y):
                    suspects.append(y)
                elif ip_tester.ip6(y):
                    suspects.append(y)

        suspects = self.remove_locals(suspects)
        print('ssh suspects:', suspects)

        already_blocked = []
        ssh_attackers = [ip for ip, count in collections.Counter(suspects).items() if count > 4]
        for x in self.known_attackers:
            if x in ssh_attackers:
                ssh_attackers.remove(x)

        print('ssh_attackers:', ssh_attackers)
        for x in ssh_attackers:
            self.attackers.append(x)

    def apache(self, log_):
        failed_attempts = []
        log = open(log_, 'r', encoding='utf8')
        for x in log:
            if re.search(r'.*(\.php).*(\s404\s)', x):
                failed_attempts.append(x)
    
        suspects = []
        for x in failed_attempts:
            possible_ip = x.split()[0]
            if ip_tester.ip4(possible_ip):
                suspects.append(possible_ip)
            elif ip_tester.ip6(possible_ip):
                suspects.append(possible_ip)
            else:
                for y in x.split()[1:]:
                    if ip_tester.ip4(y):
                        suspects.append(y)
                    elif ip_tester.ip6(y):
                        suspects.append(y)
    
        suspects = self.remove_locals(suspects)
        print('apache suspects:', suspects)
    
        already_blocked = []
        apache_attackers = [ip for ip, count in collections.Counter(suspects).items() if count > 12]
        for x in self.known_attackers:
            if x in apache_attackers:
                apache_attackers.remove(x)
        
        print('apache_attackers:', apache_attackers)
        for x in apache_attackers:
            self.attackers.append(x)
    
    def fail2ban(self, log_):
        failed_attempts = []
        log = open(log_, 'r', encoding='utf8')
        for x in log:
            if re.search(r'.*?NOTICE.*?Ban\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', x):
                failed_attempts.append(x)
    
        suspects = []
        for x in failed_attempts:
            possible_address = x.split()[-1]
            if ip_tester.ip4(possible_address):
                suspects.append(possible_address)
            elif ip_tester.ip6(possible_address):
                suspects.append(possible_address)
    
        suspects = self.remove_locals(suspects)
        print('dos suspects:', suspects)
    
        already_blocked = []
        dos_attackers = [ip for ip, count in collections.Counter(suspects).items() if count > 1]
        for x in self.known_attackers:
            if x in dos_attackers:
                dos_attackers.remove(x)
    
        print('dos_attackers:', dos_attackers)
        for x in dos_attackers:
            self.attackers.append(x)

    def remove_locals(self, suspects):
        just_me = []
        for x in suspects:
            if x.startswith('192.168.1.'):
                just_me.append(x)
                print('\nFound myself!\n')
        for x in just_me:
            suspects.remove(x)
            print('Removed myself!\n')
        
        return suspects

    def TONGUE_OF_DOOM(self):
        self.attackers = list(dict.fromkeys(self.attackers))
        print('self.attackers:', self.attackers)
        print('Blocking attackers now...')
        for x in self.attackers:
            command = 'iptables -I INPUT -s ' + x + ' -j DROP'
            os.popen(command)
            print(x, 'was blocked from gaining access to your computer!')
    

if __name__ == '__main__':
    if os.getuid() != 0:
        print('Try again as root!')
        sys.exit()
    elif input('Are you logged in as root? [y/n]\nSimply using sudo will not save the rules generated\n').lower() != 'y':
        sys.exit()
    try:
        kermit = Frog()
        kermit.auth('/var/log/auth.log')
        kermit.auth('/var/log/auth.log.1')
        kermit.apache('/var/log/apache2/access.log')
        kermit.apache('/var/log/apache2/access.log.1')
        kermit.fail2ban('/var/log/fail2ban.log')
        kermit.fail2ban('/var/log/fail2ban.log.1')
        kermit.TONGUE_OF_DOOM()
        os.popen('iptables-save > /etc/iptables/rules.v4')
    except Exception:
        print(sys.exc_info())
        print('\nKermit the frog has failed in his sacred duties as guardian of the CyberKingdom\n')
    else:
        print('\nSuccess!\n')
