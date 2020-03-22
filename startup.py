#!/usr/local/bin/python3

import os, sys, random, subprocess

if os.getuid() != 0:
    print('Try again as root!')
    sys.exit()


def start_rock64():
    if os.getcwd() != '/home/rock64/Repos/Tools':
        os.chdir('/home/rock64/Repos/Tools')
    import guestbook

    os.popen('sudo noip2')
    os.popen('sudo runuser -u rock64 boinc')

    if '/usr/lib/xorg/Xorg' in subprocess.getoutput('ps -aux | grep Xorg'):
        background = os.path.join('/home/rock64/Pictures/backgrounds', random.choice(os.listdir('/home/rock64/Pictures/backgrounds')))
        command = 'feh --bg-fill ' + background
        os.popen(command)
        os.popen('xrdb -merge /home/rock64/.Xresources')
    
    try:
        guestbook.signin('/var/log/apache2/access.log')
        guestbook.signin('/var/log/apache2/access.log.1')
    except Exception:
        with open('/home/rock64/startup_exceptions.txt', 'w') as f:
            f.write('\n' + sys.exc_info() + '\n')

    try:
        print('\nTrying updated flyswatter feature!\n')
        from flyswatter import Frog
        kermit = Frog()
        kermit.auth('/var/log/auth.log')
        kermit.auth('/var/log/auth.log.1')
        kermit.apache('/var/log/apache2/access.log')
        kermit.apache('/var/log/apache2/access.log.1')
        kermit.fail2ban('/var/log/fail2ban.log')
        kermit.fail2ban('/var/log/fail2ban.log.1')
        kermit.TONGUE_OF_DOOM()
        os.popen('iptables-save > /etc/iptables/rules.v4')
        print('\nSuccess!\n')
    except Exception:
        with open('/home/rock64/startup_exceptions.txt', 'w') as f:
            f.write('\n' + sys.exc_info() + '\n')

    os.popen('sudo iptables -A INPUT -s 222.186.0.0/16 -j DROP')
    os.popen('sudo iptables -A INPUT -s 222.187.0.0/16 -j DROP')
    os.popen('sudo iptables -A INPUT -s 218.98.0.0/16 -j DROP')
    os.popen('sudo iptables -A INPUT -s 223.111.0.0/16 -j DROP')

    print('Done!')


with open('/etc/hostname', 'r') as host:
    name = host.readline()
    #if 'blacktop' in name:
    #    start_blacktop()
    if 'rock64' in name:
        start_rock64()
