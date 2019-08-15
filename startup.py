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

    #protocol = input('\nStart VPN?\nEnter protocol: [udp/tcp]\n').lower()
    #if protocol in ['udp', 'tcp']:
        #country = input('\nEnter country (e.g. us/nam):\n').lower()
        #threading.Thread(None, tunnel, args=(country, protocol)).run()

    #why don't these work??
    #if input('\nStart pydoc? [y/n]\n').lower() == 'y':
        #os.popen('pydoc3 -b')
    #if input('\nStart tutanota client? [y/n]\n').lower() == 'y':
        #os.popen('tuta')

    #for x in os.listdir('/home/crowbar/Repos'):
        #threading.Thread(None, pull, args=(os.path.join('/home/crowbar/Repos', x), x)).run()


def start_rock64():
    import guestbook
    os.popen('sudo noip2')
    os.popen('sudo a2dissite 4v3s')
    os.popen('sudo mount -t ext4 /dev/mmcblk1p1 /srv/ftp')

    try:
        print('\nTrying new mail retrieval feature!\n')
        mail = open('/var/mail/apache', 'rb').readlines()
        if len(mail) > 0:
            print("\nYou've got mail!")
            envelope = os.open('/home/rock64/Documents/message', os.O_CREAT | os.O_WRONLY | os.O_APPEND)
            os.write(envelope, mail)
            os.close(envelope)
            mail.close()
            empty = open('/var/mail/apache', 'wb')
            empty.write(b'')
            empty.close()
        else:
            mail.close()
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
        except Exception:
            print('\nFlyswatter feature failed! Exception info to follow:\n')
            print(sys.exc_info())

    #for x in os.listdir('/home/rock64/Repos'):
        #threading.Thread(None, pull, args=(os.path.join('/home/rock64/Repos', x), x)).run()

    print('Done!')


with open('/etc/hostname', 'r') as host:
    name = host.readline()
    if 'blacktop' in name:
        start_blacktop()
    elif 'rock64' in name:
        start_rock64()
