#!/bin/bash

# must do "sudo systemctl start nfs-kernel-server" on rock64 first!
# sudo mount -t nfs 192.168.1.64:/srv /mnt/nfs
cd /home/crowbar
sudo rsync -aAv --delete --exclude=.cache /home/crowbar /media/crowbar/'Seagate Backup Plus Drive'/backupDocs/rsync
sudo rsync -aAv --delete /mnt/nfs /media/crowbar/'Seagate Backup Plus Drive'/backupDocs/rsync/rock64
echo Done!
