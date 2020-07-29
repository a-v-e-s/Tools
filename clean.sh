#!/bin/bash

if [ "$EUID" -ne 0 ]; then
        echo This script must be run as root!
        exit
fi

rm -r --interactive=never /home/*/.cache/thumbnails

echo '' > /home/*/.bash_history
echo '' > /home/*/.sqlite_history
echo '' > /home/*/.python_history
echo '' > /root/.bash_history
echo '' > /root/.python_history

