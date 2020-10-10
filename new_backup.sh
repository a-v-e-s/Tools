#!/bin/bash

# this script should be run as root:
if [[ "$UID" -ne 0 ]];
then
	echo "This script must be run as root:"
	echo "use \"su root; ./script_name.sh\","
	echo "and not \"sudo ./script_name.sh\"."
	exit 2
fi

# exit if any errors detected:
set -e

# detect & unmount encfs virtual filesystems:
if [[ -n `df | grep encfs` ]]
then
	fss=`df | grep encfs | awk '{print $6}'`
	for fs in "$fss"
	do
		fusermount -u "$fs"
	done
fi

# mount windows disk and encrypted backup drive:
win_disk=`ls /dev | grep -e sd[ab]4`
mount /dev/$win_disk /mnt/hdd
zuluCrypt-cli -o -d /dev/sdc2 -m Seagate -e rw -h

# sometimes rsync commands raise errors while mostly working:
set +e
# remember not to put "/" after end directory names, because it changes the behavior:
rsync -aAv --delete --exclude=.cache /home/aves /run/media/private/root/Seagate/backup_docs/rsync/debi
rsync -av --delete /mnt/hdd/Users/jdtan  /run/media/private/root/Seagate/backup_docs/rsync/windows

# create a weekly tarball of the most important files:
echo "Push tarball of most important files to mega? [y/n]"
read reply
if [[ "$reply" = y ]]
then
	pushd /run/media/private/root/Seagate/backup_docs
	fn=`date +%F`_essential.tar.gz
	tar -czvf "$fn" rsync/debi/aves/{Documents,Pictures,Music,Repos,.crypt3} \
		rsync/windows/jdtan/Documents/My\ Games/XMage/my_files
	echo "Enter username/email for mega.nz:"
	read un
	megaput "$fn" -u "$un"
	popd
fi

# unmount the drives:
umount /mnt/hdd
zuluCrypt-cli -q -d /dev/sdc2

echo DONE!