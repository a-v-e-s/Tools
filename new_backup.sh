#!/bin/bash

# "sudo systemctl start nfs-kernel-server"  or start nfs-server with startup.py on rock64 first!
echo "Is nfs-kernel-server running on rock64? [y/n]"
read REPLY
if [[ "$REPLY" != [Yy] ]]; then
	echo "You must first start nfs-kernel-server on your rock64!"
	exit 2
fi

# make sure this is being run as root:
if [ "$EUID" -ne 0 ]; then
	echo This script must be run as root!
	exit 2
fi

set -e # exit if there are any errors for the next few parts

_user=aves
_home=/home/aves

# make sure Seagate Backup Drive is mounted:
if ! [[ -d /media/$_user/backupDocs/ ]]; then
	sudo mount /dev/sdc1 /media/$_user/
fi

# mount rock64
ROCK64=$(
	sudo arp-scan --localnet | \
	egrep "2a:90:45:d6:eb:3e" | \
	cut -f 1
)
ROCK64=$(
	echo $ROCK64 | \
	cut --delimiter=' ' -f 1
)

sudo mount -t nfs $ROCK64: /mnt/nfs
sudo mount /dev/sda4 /mnt/hdd

# now change into home directory and run rsync commands!
cd $_home
set +e 		# I think unimportant rsync errors may have caused this to exit prematurely
sudo rsync -aAv --delete /mnt/nfs /media/$_user/backupDocs/rsync/rock64
sudo rsync -av --delete /mnt/hdd/Users/jdtan /media/$_user/backupDocs/rsync/Windows
sudo rsync -aAv --delete --exclude=.cache $_home /media/$_user/backupDocs/rsync/linux_blacktop

sudo umount /mnt/nfs
sudo umount /mnt/hdd

echo Done!
