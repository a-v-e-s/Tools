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

# find out who we are
# set local $_user and $_home variables
# necessary because `sudo bash scriptname` creates subshell where $USER=root
# and you can't `sudo source scriptname` because source is a builtin
if [[ -d /home/crowbar ]]; then
	_user=crowbar
	_home=/home/crowbar
elif [[ -d /home/aves ]]; then 
	_user=aves
	_home=/home/aves
fi

# make sure Seagate Backup Drive is mounted:
if ! [[ -d /media/$_user/Seagate\ Backup\ Plus\ Drive/ ]]; then
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
mount -t nfs $ROCK64: /mnt/nfs

# mount other storage drives in the correct locations:
ROOT_DEV=`cat /etc/mtab | grep "sd[ab][1-5] / " | cut -d " " -f1 | cut -d "/" -f3`
case "$ROOT_DEV" in
	sdb2)
		PARROT=/mnt/hdd2
		sudo mount /dev/sda4 /mnt/hdd
		sudo mount /dev/sdb4 $PARROT
		;;
	sda2)
		PARROT=/mnt/hdd2
		sudo mount /dev/sdb4 /mnt/hdd
		sudo mount /dev/sda4 $PARROT
		;;
	sdb4)
		DEBIAN=/mnt/hdd2
		sudo mount /dev/sda4 /mnt/hdd
		sudo mount /dev/sdb2 $DEBIAN
		;;
	sda4)
		DEBIAN=/mnt/hdd2
		sudo mount /dev/sdb4 /mnt/hdd
		sudo mount /dev/sda2 $DEBIAN
		;;
	*)
		echo "Storage drives are not at their expected locations in /dev/.\nExiting now."
		exit 2
		;;
esac

# now change into home directory and run rsync commands!
cd $_home
set +e 		# I think unimportant rsync errors may have caused this to exit prematurely
sudo rsync -aAv --delete $_home/Mutual /media/$_user/Seagate\ Backup\ Plus\ Drive/backupDocs/rsync
sudo rsync -aAv --delete /mnt/nfs /media/$_user/Seagate\ Backup\ Plus\ Drive/backupDocs/rsync/rock64
sudo rsync -av --delete /mnt/hdd/Users/jdtan /media/$_user/Seagate\ Backup\ Plus\ Drive/backupDocs/rsync/Windows
if [[ "$_user" == "crowbar" ]]; then
	sudo rsync -aAv --delete --exclude=.cache --exclude=Mutual $_home /media/$_user/Seagate\ Backup\ Plus\ Drive/backupDocs/rsync/debi
	sudo rsync -aAv --delete --exclude=.cache /mnt/hdd2/home/aves /media/$_user/Seagate\ Backup\ Plus\ Drive/backupDocs/rsync
elif [[ "$_user" == "aves" ]]; then
	sudo rsync -aAv --delete --exclude=.cache --exclude=Mutual $_home /media/$_user/Seagate\ Backup\ Plus\ Drive/backupDocs/rsync
	sudo rsync -aAv --delete --exclude=.cache /mnt/hdd2/home/crowbar /media/$_user/Seagate\ Backup\ Plus\ Drive/backupDocs/rsync/debi
fi

sudo umount /mnt/nfs
sudo umount /mnt/hdd
sudo umount /mnt/hdd2
echo Done!
