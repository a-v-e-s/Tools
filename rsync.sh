#!/bin/bash

# "sudo systemctl start nfs-kernel-server"  or start nfs-server with startup.py on rock64 first!
# then sudo mount -t nfs 192.168.1.xxx:/srv /mnt/nfs
cd /home/crowbar
sudo rsync -aAv --delete --exclude=.cache /home/crowbar /media/crowbar/'Seagate Backup Plus Drive'/backupDocs/rsync
sudo rsync -aAv --delete /mnt/nfs /media/crowbar/'Seagate Backup Plus Drive'/backupDocs/rsync/rock64
echo Done!
