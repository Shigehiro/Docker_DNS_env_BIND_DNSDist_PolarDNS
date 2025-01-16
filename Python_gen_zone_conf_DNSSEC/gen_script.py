#!/usr/bin/env python3

import subprocess

start = 0
#end = 100
#step = 10
end = 300000
step = 50000
sleep_time = 1200

with open('gen_dnssec_conf.sh', 'w') as f:
    f.write("#!/bin/sh\n\n")
    f.write("# script01\n")
    for i in range(0, end, step):
        if i != end:
            str01 = f"python3 ./generate_sub.sub.example.com.py -s {i} -e {i+step} &"
            str02 = f"python3 ./generate_sub.sub.delay.com.py -s {i} -e {i+step} &"
            f.write(f"{str01}\n")
            f.write(f"{str02}\n")
        #if i == 270000:
        if i == (end - step):
            str01 = f"python3 ./generate_sub.sub.example.com.py -s {i} -e {i+step} &"
            str02 = f"python3 ./generate_sub.sub.delay.com.py -s {i} -e {i+step}"
            f.write(f"{str01}\n")
            f.write(f"{str02}\n")
            f.write(f"sleep {sleep_time}\n")

with open('gen_dnssec_conf.sh', 'a') as f:
    f.write("\n# script02\n")
    for i in range(0, end, step):
        if i != end:
            str01 = f"python3 ./generate_sub.sub.delay.com_02.py -s {start} -e {end} &"
            f.write(f"{str01}\n")
        if i == (end - step):
            str01 = f"python3 ./generate_sub.sub.delay.com_02.py -s {start} -e {end}"
            f.write(f"{str01}\n")
            f.write(f"sleep {sleep_time}\n")

with open('gen_dnssec_conf.sh', 'a') as f:
    f.write("\n# script03\n")
    str01 = f"python3 ./generate_com_root_named.conf.py -s {start} -e {end}"
    f.write(f"{str01}\n")

cmd01 = 'chmod +x ./gen_dnssec_conf.sh'
p = subprocess.run(cmd01.split(), capture_output=True, text=True)
