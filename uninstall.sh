#!/usr/bin/bash

if [ "${EUID}" -ne 0 ]; then
    echo "Error: you must run this script as root";
    exit 1;
fi

if ! rm /usr/bin/ack; then
    echo "Error: couldn't remove execute 'ack' file in /usr/bin";
    exit 1;
fi

if ! rm /usr/bin/rack; then
    echo "Error: couldn't remove execute 'rack' file in /usr/bin";
    exit 1;
fi

echo "Uninstall was successful"
exit 0