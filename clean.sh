#!/bin/bash

if [ "$EUID" -ne 0 ]; then
        echo This script must be run as root!
        exit
fi

rm -r --interactive=never /home/$USER/.cache/thumbnails
echo '' > /home/$USER/.bash_history
echo '' > /home/$USER/.sqlite_history
echo '' > /home/$USER/.python_history
echo '' > /root/.bash_history
echo '' > /root/.python_history

