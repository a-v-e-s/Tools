#!/bin/bash

if [ "$EUID" -ne 0 ]; then
	echo This script must be run as root!
	exit
fi

if [ -f /root/clamscan_results.txt ]; then
    rm /root/clamscan_results.txt
fi

if [ $(cat /etc/hostname) == "blacktop" ]; then
    declare -a directories=(
        "/bin"
        "/boot"
        "/etc"
        "/home"
        "/lib"
        "/lib32"
        "/lib64"
        "/libx32"
        "/root"
        "/sbin"
        "/usr"
        "/var"
    )
fi

if [ $(cat /etc/hostname) == "rock64" ]; then
    declare -a directories=(
        "/bin"
        "/boot"
        "/etc"
        "/home"
        "/lib"
        "/root"
        "/sbin"
        "/srv"
        "/usr"
        "/var"
    )
fi

for i in "${directories[@]}"; do
    echo scanning $i
    # can I run these in parallel without consuming an obscene amount of memory?
    # tried it with "&" at the end of them command,
    # but this quickly caused the system to start using swap :(
    clamscan -ir --max-filesize=25M $i >> /root/clamscan_results.txt
done

cat /root/clamscan_results.txt
echo Done!