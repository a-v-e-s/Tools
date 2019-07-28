#!/bin/bash

# "sudo systemctl start nfs-kernel-server"  or start nfs-server with startup.py on rock64 first!
# then sudo mount -t nfs 192.168.1.xxx: /mnt/nfs
# sudo mount /dev/sda? /mnt/nfs
# if you configure your server & router to give the same ip to the server, you can uncomment the previous line
cd /home/crowbar
sudo rsync -aAv --delete --exclude=.cache /home/crowbar /media/crowbar/'Seagate Backup Plus Drive'/backupDocs/rsync/debi
sudo rsync -aAv --delete /mnt/nfs /media/crowbar/'Seagate Backup Plus Drive'/backupDocs/rsync/rock64
sudo rsync -aAv --delete /mnt/hdd/Users/jdtan /media/crowbar/'Seagate Backup Plus Drive'/backupDocs/rsync/Windows
echo Done!
