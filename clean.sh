#!/bin/bash

if [ "$EUID" -ne 0 ]; then
        echo This script must be run as root!
        exit
fi

rm -r --interactive=never /home/crowbar/.cache/thumbnails
echo '' > /home/crowbar/.bash_history
echo '' > /home/crowbar/.sqlite_history
echo '' > /home/crowbar/.python_history
echo '' > /root/.bash_history
echo '' > /root/.python_history

