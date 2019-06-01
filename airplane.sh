#!/bin/bash
# 2 lines to put your laptop into airplane mode
# "chown root airplane", "chmod +x airplane", remove .sh extension,
# copy to /bin directory or another on PATH, 
# and run with "sudo airplane" for best results :)

sudo rfkill block bluetooth
sudo rfkill block wifi

