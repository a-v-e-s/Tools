#!/usr/local/bin/python3

import os, sys, random, subprocess, threading
#from pull import pull
#from tunnel import tunnel

if os.getuid() != 0:
    print('Try again as root!')
    sys.exit()


def start_blacktop():
    os.popen('sudo rfkill block bluetooth')
    os.popen('rm -r --interactive=never /home/crowbar/.cache/thumbnails')
    os.popen('echo '' > /home/crowbar/.bash_history')
    os.popen('echo '' > /home/crowbar/.sqlite_history')
    if input('\nAirplane mode? [y/n]\n').lower() == 'y':
        os.popen('sudo rfkill block wifi')

    #print('\nTrying new feature to mount internal drive on startup!\n')
    #if 'sda5' in subprocess.getoutput('ls /dev'):
    #    os.popen('sudo mount /dev/sda4 /mnt/hdd')
    #elif 'sdb5' in subprocess.getoutput('ls /dev'):
    #    os.popen('sudo mount /dev/sdb4 /mnt/hdd')
    #else:
    #    print('\nCould not find and mount internal hard drive!\n')

    #why don't these work??
    #if input('\nStart pydoc? [y/n]\n').lower() == 'y':
        #os.popen('pydoc3 -b')
    #if input('\nStart tutanota client? [y/n]\n').lower() == 'y':
        #os.popen('tuta')


def start_rock64():
    import guestbook
    if os.getcwd() != '/home/rock64/Repos/Tools':
        os.chdir('/home/rock64/Repos/Tools')

    os.popen('sudo noip2')
    os.popen('sudo systemctl start ssh')
    os.popen('xrdb -merge /home/rock64/.Xresources')
    """
    try:
        print('\nTrying new mail retrieval feature!\n')
        mail = open('/var/mail/apache', 'r').readlines()
        if len(mail) > 2:
            print("\nYou've got mail!")
            envelope = os.open('/home/rock64/Mail/message', 'a')
            abyss = envelope.write(envelope, mail)
            envelope.close()
            mail.close()
            empty = open('/var/mail/apache', 'wb')
            empty.write(b'')
            empty.close()
        else:
            mail.close()
    except Exception:
        print('\nTried to deliver mail but failed. Exception info to follow:\n')
        print(sys.exc_info())
    """
    if '/usr/lib/xorg/Xorg' in subprocess.getoutput('ps -aux | grep Xorg'):
        background = os.path.join('/home/rock64/Pictures/backgrounds', random.choice(os.listdir('/home/rock64/Pictures/backgrounds')))
        command = 'feh --bg-fill ' + background
        os.popen(command)

    if input('\nStart Owncloud? [y/n]\n').lower() == 'y':
        os.popen('sudo a2ensite 4v3s')
        os.popen('sudo systemctl reload apache2')
        os.popen('sudo systemctl start mysql')

    if input('\nStart nfs server for home directory? [y/n]\n').lower() == 'y':
        os.popen('sudo systemctl start nfs-kernel-server')
    
    if input('\nStart XMage server? [y/n]\n').lower() == 'y':
        os.chdir('/home/rock64/XMAGE/xmage/mage-server')
        try:
            os.popen('java -Xms256M -Xmx512M -XX:MaxPermSize=256m -Djava.security.policy=./config/security.policy -Djava.util.logging.config.file=./config/logging.config -Dlog4j.configuration=file:./config/log4jproperties -jar lib/mage-server-1.4.39.jar')
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
            print('\nTrying new flyswatter feature!\n')
            import flyswatter
            flyswatter.auth('/var/log/auth.log')
            flyswatter.apache('/var/log/apache2/access.log')
            os.popen('iptables-save > /etc/iptables/rules.v4')
            print('\nSuccess!\n')
        except Exception:
            print('\nFlyswatter feature failed! Exception info to follow:\n')
            print(sys.exc_info())


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
