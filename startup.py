#!/usr/local/bin/python3

import os, sys, random, subprocess, threading
#from pull import pull
#from tunnel import tunnel

if os.getuid() != 0:
    print('Try again as root!')
    sys.exit()


def start_blacktop():
    print('this function is obsolete, you turd.')


def start_rock64():
    import guestbook
    if os.getcwd() != '/home/rock64/Repos/Tools':
        os.chdir('/home/rock64/Repos/Tools')

    os.popen('sudo noip2')
    os.popen('sudo systemctl start ssh')
    os.popen('xrdb -merge /home/rock64/.Xresources')

    if '/usr/lib/xorg/Xorg' in subprocess.getoutput('ps -aux | grep Xorg'):
        background = os.path.join('/home/rock64/Pictures/backgrounds', random.choice(os.listdir('/home/rock64/Pictures/backgrounds')))
        command = 'feh --bg-fill ' + background
        os.popen(command)
        
    if input('\nStart vsftpd [y/n]\n').lower() == 'y':
        os.popen('sudo vsftpd')

    if input('\nStart Owncloud? [y/n]\n').lower() == 'y':
        os.popen('sudo a2ensite 4v3s')
        os.popen('sudo systemctl reload apache2')
        os.popen('sudo systemctl start mysql')

    if input('\nStart nfs server for home directory? [y/n]\n').lower() == 'y':
        os.popen('sudo systemctl start nfs-kernel-server')
    
    if input('\nStart XMage server? [y/n]\n').lower() == 'y':
        os.chdir('/home/rock64/XMAGE/xmage/mage-server')
        xmage_command = """
            java -Xms256M -Xmx512M -XX:MaxPermSize=256m 
            -Djava.security.policy=./config/security.policy 
            -Djava.util.logging.config.file=./config/logging.config 
            -Dlog4j.configuration=file:./config/log4jproperties 
            -jar lib/mage-server-1.4.39.jar
        """
        try:
            os.popen(xmage_command)
        except Exception:
            print('Starting XMage server failed. Exception info to follow:')
            print(sys.exc_info())

    try:
        print('\nTrying new guestbook feature!\n')
        guestbook.signin('/var/log/apache2/access.log')
    except Exception:
        print('\nGuestbook feature failed. Exception info to follow:\n')
        print(sys.exc_info())

    if input('Are you *logged in as root*? [y/n]\nMerely using "sudo" will not work\nEntering y will run flyswatter.py\n').lower() != 'y':
        print('Done!')
        sys.exit()
    else:
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
            print(sys.exc_info())
            print('\nKermit the frog has failed in his sacred duties as guardian of the CyberKingdom\n')

    os.popen('sudo iptables -A INPUT -s 222.186.0.0/16 -j DROP')
    os.popen('sudo iptables -A INPUT -s 222.187.0.0/16 -j DROP')
    os.popen('sudo iptables -A INPUT -s 218.98.0.0/16 -j DROP')
    os.popen('sudo iptables -A INPUT -s 223.111.0.0/16 -j DROP')

    print('Done!')


with open('/etc/hostname', 'r') as host:
    name = host.readline()
    if 'blacktop' in name:
        start_blacktop()
    elif 'rock64' in name:
        start_rock64()
