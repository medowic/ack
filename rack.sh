#!/usr/bin/bash

if [ "${EUID}" -ne 0 ]; then
    echo "Error: you must run this script as root or with 'sudo'";
    exit 1;
fi

export SUDO_USER=root
export USER=${USER}
export ACK_CHANGED_ROOT=True

if [ "${1}" == "-l" ] || [ "${1}" == "--list" ]; then
    su root -c "ack -l";
elif [ "${1}" == "-s" ] || [ "${1}" == "--stop" ]; then
    su root -c "ack -s ${2}";
elif [ "${1}" == "-r" ] || [ "${1}" == "--restart" ]; then
    su root -c "ack -r ${2}";
else
    su root -c "ack main.py $*";
fi