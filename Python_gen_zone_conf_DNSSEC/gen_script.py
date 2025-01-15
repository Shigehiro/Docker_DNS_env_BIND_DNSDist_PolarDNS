#!/usr/bin/env python3

import subprocess

start = 0
end = 100
step = 10
#end = 300000
#step = 50000

with open('gen_dnssec_conf_01.sh', 'w') as f:
    f.write("#!/bin/sh\n\n")
    for i in range(0, end, step):
        str01 = f"python3 ./generate_sub.sub.example.com.py -s {i} -e {i+step} &"
        str02 = f"python3 ./generate_sub.sub.delay.com.py -s {i} -e {i+step} &"
        f.write(f"{str01}\n")
        f.write(f"{str02}\n")

with open('gen_dnssec_conf_02.sh', 'w') as f:
    f.write("#!/bin/sh\n\n")
    for i in range(0, end, step):
        str01 = f"python3 ./generate_sub.sub.delay.com_02.py -s {start} -e {end} &"
        f.write(f"{str01}\n")

with open('gen_dnssec_conf_03.sh', 'w') as f:
    f.write("#!/bin/sh\n\n")
    str01 = f"python3 ./generate_com_root_named.conf.py -s {start} -e {end}"
    f.write(f"{str01}\n")

cmd01 = 'chmod +x ./gen_dnssec_conf_01.sh'
cmd02 = 'chmod +x ./gen_dnssec_conf_02.sh'
cmd03 = 'chmod +x ./gen_dnssec_conf_03.sh'
p = subprocess.run(cmd01.split(), capture_output=True, text=True)
p = subprocess.run(cmd02.split(), capture_output=True, text=True)
p = subprocess.run(cmd03.split(), capture_output=True, text=True)
