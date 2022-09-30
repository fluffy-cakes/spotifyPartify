#!/bin/bash

if [ -f ./db.sqlite3 ]; then
    echo "DELETING LOCAL DB"
    rm -f ./db.sqlite3
fi

if [ -f ./users.json ]; then
    echo "DELETING LOCAL USERS"
    rm -f ./users.json
fi


echo "$WEDDING_USERS" > users.json
uname -a
sleep 2

python3 db_setup.py
ls -lah /app
