#!/bin/bash

# RUN THIS IN THE tuprware-node/ DIRECTORY
gunicorn --workers 3 --bind unix:app.sock -m 777 --daemon wsgi:app
if [ $? -eq 0 ]; then
    echo "Node started."
else
    echo "Something went wrong..."
fi