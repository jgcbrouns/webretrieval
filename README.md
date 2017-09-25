README File For Webretrieval

Section (1) - Database connection

You can connect with mongo database via a GUI client like for example; RoboMongo (many others are out there). In your client, use the following credidentials:

servername:  109.238.10.185
port:        27000
database:    webretrieval
username:    webretrieval
password:    tue


We need a so called ‘driver’ to enable our python scripts to communicate with the database. You can install it like so:
MAC/LINUX mongoDB driver:

1.  install mongoDB driver for python:
2.  download pip-installer script at https://bootstrap.pypa.io/get-pip.py
3.  open a temrinal in the same window as the script you just downloaded
4.  run:    python get-pip.py
5.  run:    python -m pip install pymongo

WINDOWS:
google
