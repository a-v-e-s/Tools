#!/bin/bash

# "sudo systemctl start nfs-kernel-server"  or start nfs-server with startup.py on rock64 first!

# make sure this is being run as root:
if [ "$EUID" -ne 0 ]; then
	echo This script must be run as root!
	exit
fi

# mount your server via nfs!
# this doesn't work well.
# mount -t ... takes too long and "&& break" doesn't exit the for loop for some reason.
#for x in {64..253}; do
#	address=192.168.1.$x:
#	(mount -t nfs $address /mnt/nfs && break;)
#done

#mount your internal (windows) hard drive!
read sd < <(ls /dev | egrep sd[abcd]5)
hdd=/dev/$sd
mount $hdd /mnt/hdd

# now change into home directory and run rsync commands!
cd /home/crowbar
sudo rsync -aAv --delete --exclude=.cache /home/crowbar /media/crowbar/'Seagate Backup Plus Drive'/backupDocs/rsync/debi
sudo rsync -aAv --delete /mnt/nfs /media/crowbar/'Seagate Backup Plus Drive'/backupDocs/rsync/rock64
sudo rsync -aAv --delete /mnt/hdd/Users/jdtan /media/crowbar/'Seagate Backup Plus Drive'/backupDocs/rsync/Windows
echo Done!
