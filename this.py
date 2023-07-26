from time import sleep
import datetime as dt
import os
import sys

sleep(123)

while True:
    a = open("ping", 'r').read()
    if a == "==off==": continue
    c = dt.datetime(int(a.split()[0].split('-')[0]), int(a.split()[0].split('-')[1]), int(a.split()[0].split('-')[2]), int(a.split()[1].split(':')[0]), int(a.split()[1].split(':')[1]), int(a.split()[1].split('.')[0].split(':')[2]))
    delta = dt.datetime.now() - c
    if delta.total_seconds() > 120:
        os.system(f"python3 {sys.argv[1]} -rec &")
    sleep(29)
