function clean {
    # make sure we are NOT root:
    if [[ $EUID -eQ 0 ]];
    then
        echo "Must NOT be run as root!"
        exit 11
    fi

    # 
    echo '' > /home/"$USER"/.bash_history
    echo '' > /home/"$USER"/.sqlite_history
    echo '' > /home/"$USER"/.python_history
    # only execute the second sudo statement if the first one succeeds:
    sudo echo '' > /root/.bash_history; \
    && \
    sudo echo '' > /root/.sqlite_history; \
    sudo echo '' > /root/.python_history

}

function get_total_time {
    end_time=`date +%s`
    total_time=$(( $end_time - $1 ))
    echo $total_time
}

function urandomize {
    # make sure we are root:
    if [[ $EUID -ne 0 ]];
    then
        echo "Must be run as root!"
        exit 10
    fi

    # get name of device-file in /dev/ :
    echo "Name of device in /dev/ to urandom-ly overwrite:\n"
    read dev_name

    # urandomize the device-file and report on results
    start_time=`date +%s`
    sudo dd bs=1M if=/dev/urandom of=/dev/"$dev_name" \
    && \
    total=`get_total_time $start_time`
    echo "SUCCESS in $total seconds"; \
    || \
    echo "Failure; exit code $? in $total seconds"

}

# Aliases:
if [[ -f ~/.bash_aliases ]]
then
    source ~/.bash_aliases
else
    alias fucking='sudo'
    # hehe
    alias open='xdg-open'
    alias ls='ls --color=auto'
    alias la='ls -a --color=auto'
    alias ll='ls -al --color=auto'
    alias mv='mv -i'
    alias cp='cp -i'
    alias rm='rm -i'
    alias mkdir='mkdir -p'
    alias shred='shred -uz'
    alias dir='dir --color=auto'
    alias vdir='vdir --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
    alias jupyter='python3 -m jupyterlab'
    alias ..='cd ..'
    alias ...='cd ../..'
    alias ....='cd ../../..'
    alias .....='cd ../../../..'
    alias ......='cd ../../../../..'
    alias .......='cd ../../../../../..'
    alias ........='cd ../../../../../../..'
    alias .........='cd ../../../../../../../..'
    alias ..........='cd ../../../../../../../../..'
    alias ...........='cd ../../../../../../../../../..'
    alias ............='cd ../../../../../../../../../../..'
fi