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
    os.popen('sudo a2dissite 4v3s')
    os.popen('sudo mount -t ext4 /dev/mmcblk1p1 /srv/ftp')

    try:
        print('\nTrying new mail retrieval feature!\n')
        mail = open('/var/mail/apache', 'rb').readlines()
        if len(mail) > 0:
            print("\nYou've got mail!")
            envelope = os.open('/home/rock64/Mail/message', os.O_CREAT | os.O_WRONLY | os.O_APPEND)
            os.write(envelope, mail)
            os.close(envelope)
            mail.close()
            empty = open('/var/mail/apache', 'wb')
            empty.write(b'')
            empty.close()
        del mail
    except Exception:
        print('\nTried to deliver mail but failed. Exception info to follow:\n')
        print(sys.exc_info())

    if input('\nStart ssh server? [y/n]\n').lower() == 'y':
        os.popen('sudo systemctl start ssh')

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
            
    print('Done!')

    os.popen('sudo iptables -A INPUT -s 222.186.0.0/16 -j DROP')
    os.popen('sudo iptables -A INPUT -s 222.187.0.0/16 -j DROP')
    os.popen('sudo iptables -A INPUT -s 218.98.0.0/16 -j DROP')
    os.popen('sudo iptables -A INPUT -s 223.111.0.0/16 -j DROP')


with open('/etc/hostname', 'r') as host:
    name = host.readline()
    if 'blacktop' in name:
        start_blacktop()
    elif 'rock64' in name:
        start_rock64()
