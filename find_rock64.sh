#!/bin/bash

rock64=$(
        sudo arp-scan --localnet | \
        egrep "2a:90:45:d6:eb:3e" | \
        cut -f 1
)

echo rock64: $rock64
