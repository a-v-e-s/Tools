#!/bin/bash

# "sudo systemctl start nfs-kernel-server"  or start nfs-server with startup.py on rock64 first!

# make sure this is being run as root:
if [ "$EUID" -ne 0 ]; then
	echo This script must be run as root!
	exit
fi

# mount rock64
rock64=$(
	sudo arp-scan --localnet | \
	egrep "2a:90:45:d6:eb:3e" | \
	cut -f 1
)
rock64=$(
	echo $rock64 | \
	cut --delimiter=' ' -f 1
)
sudo mount -t nfs $rock64: /mnt/nfs

# mount your internal (windows) hard drive!
read sd < <(ls /dev | egrep sd[abcd]4)
hdd=/dev/$sd
sudo mount $hdd /mnt/hdd

# now change into home directory and run rsync commands!
cd /home/crowbar
sudo rsync -aAv --delete --exclude=.cache /home/crowbar /media/crowbar/'Seagate Backup Plus Drive'/backupDocs/rsync/debi
sudo rsync -aAv --delete /mnt/nfs /media/crowbar/'Seagate Backup Plus Drive'/backupDocs/rsync/rock64
sudo rsync -aAv --delete /mnt/hdd/Users/jdtan /media/crowbar/'Seagate Backup Plus Drive'/backupDocs/rsync/Windows
echo Done!
