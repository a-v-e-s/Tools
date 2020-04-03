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

# make sure Seagate Backup Drive is mounted:
if ! [[ -d /media/$USER/Seagate\ Backup\ Plus\ Drive/ ]]; then
	sudo mount /dev/sdc1 /media/$USER/
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
mount -t nfs $ROCK64: /mnt/nfs

# mount other storage drives in the correct locations:
ROOT_DEV=`cat /etc/mtab | grep "sd[ab][1-5] / " | cut -d " " -f1 | cut -d "/" -f3`
if [[ "$ROOT_DEV" == sdb2 ]]; then
	PARROT=/mnt/hdd2
	sudo mount /dev/sda4 /mnt/hdd
	sudo mount /dev/sdb4 $PARROT
elif [[ "$ROOT_DEV" == sda2 ]]; then
	PARROT=/mnt/hdd2
	sudo mount /dev/sdb4 /mnt/hdd
	sudo mount /dev/sda4 $PARROT
elif [[ "$ROOT_DEV" == sdb4 ]]; then
	DEBIAN=/mnt/hdd2
	sudo mount /dev/sda4 /mnt/hdd
	sudo mount /dev/sdb2 $DEBIAN
elif [[ "$ROOT_DEV" == sda4 ]]; then
	DEBIAN=/mnt/hdd2
	sudo mount /dev/sdb4 /mnt/hdd
	sudo mount /dev/sda2 $DEBIAN
else
	echo "Storage drives are not at their expected locations in /dev/.\nExiting now."
	exit 2
fi

# now change into home directory and run rsync commands!
cd $HOME
sudo rsync -aAv --delete $HOME/Mutual /media/$USER/Seagate\ Backup\ Plus\ Drive/backupDocs/rsync
sudo rsync -aAv --delete /mnt/nfs /media/$USER/Seagate\ Backup\ Plus\ Drive/backupDocs/rsync/rock64
sudo rsync -av --delete /mnt/hdd/Users/jdtan /media/$USER/Seagate\ Backup\ Plus\ Drive/backupDocs/rsync/Windows
if [[ "$USER" == "crowbar" ]]; then
	sudo rsync -aAv --delete --exclude=.cache --exclude=Mutual $HOME /media/$USER/Seagate\ Backup\ Plus\ Drive/backupDocs/rsync/debi
	sudo rsync -aAv --delete --exclude=.cache /mnt/hdd2/home/aves /media/$USER/Seagate\ Backup\ Plus\ Drive/backupDocs/rsync
elif [[ "$USER" == "aves" ]]; then
	sudo rsync -aAv --delete --exclude=.cache --exclude=Mutual $HOME /media/$USER/Seagate\ Backup\ Plus\ Drive/backupDocs/rsync
	sudo rsync -aAv --delete --exclude=.cache /mnt/hdd2/home/crowbar /media/$USER/Seagate\ Backup\ Plus\ Drive/backupDocs/rsync/debi
fi

sudo umount /mnt/nfs
sudo umount /mnt/hdd
sudo umount /mnt/hdd2
echo Done!
