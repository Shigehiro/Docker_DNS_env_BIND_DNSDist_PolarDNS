#!/usr/bin/env python3

import argparse
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--start', type=int, required=True, help='specify the start zone index')
parser.add_argument('-e', '--end', type=int, required=True, help='specify the end zone index')
args = parser.parse_args()
start = args.start
end = args.end

zone_prefix = 'sub'
zone_suffix = 'example.com'
zone_suffix_delay = 'delay.com'

### START: sub[6digits].sub[6digits].delay.com

# Generate zone file for sub.sub.delay.com
for i in range(start, end):
    domain_number = str(f"{i:06}")
    with open(f'../bind_config_dnssec/sub.sub.delay.com/records/sub.sub.delay.com{domain_number}.template.db', 'w') as f:
        conf_string = """
$TTL 1
@ IN SOA ns01 ns01 (
2010062303
1h
15m
30d
1h )
  IN NS ns01
  IN NS ns02

ns01 IN A 192.168.55.61
ns02 IN A 192.168.55.62
ns01 IN AAAA 2001:db8:1::61
ns02 IN AAAA 2001:db8:1::62
* IN A 127.0.0.1
* IN AAAA ::1
* IN TXT 'hello'
"""
        f.write(conf_string)

for i in range(start, end):
    domain_number = str(f"{i:06}")

    if i == start:
        cmd_gen_zsk = f"dnssec-keygen -a RSASHA256 -b 1024 sub{domain_number}.sub{domain_number}.delay.com"
        cmd_gen_ksk = f"dnssec-keygen -a RSASHA256 -b 2048 -f KSK sub{domain_number}.sub{domain_number}.delay.com"
        cmd_gen_signzone = f"dnssec-signzone -e 20501231000000 -S -o sub{domain_number}.sub{domain_number}.delay.com sub.sub.delay.com{domain_number}.template.db"
        rm_file = f"rm -f ./sub.sub.delay{domain_number}.com.template.db"

        #print(f"domain : sub{domain_number}.sub{domain_number}.delay.com")
        # zsk
        p1 = subprocess.run(cmd_gen_zsk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
        zsk_suffix = str(p1.stdout).strip().replace(f"Ksub{domain_number}.sub{domain_number}.delay.com.", '')
        zsk_public = str(p1.stdout).strip() + ".key"
        zsk_private = str(p1.stdout).strip() + ".private"
        
        # ksk
        p2 = subprocess.run(cmd_gen_ksk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
        ksk_suffix = str(p2.stdout).strip().replace(f"Ksub{domain_number}.sub{domain_number}.delay.com.", '')
        ksk_public = str(p2.stdout).strip() + ".key"
        ksk_private = str(p2.stdout).strip() + ".private"

        # sing the zone
        #print(f"print cmd {cmd_gen_signzone}")
        p3 = subprocess.run(cmd_gen_signzone.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
        p = subprocess.run(rm_file.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")

    else:
        key_prefix = f"Ksub{domain_number}.sub{domain_number}.delay.com."
        
        # copy zsk, ksk files
        p = subprocess.run(['cp', zsk_private, f"{key_prefix}{zsk_suffix}.private"], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
        p = subprocess.run(['cp', zsk_public, f"{key_prefix}{zsk_suffix}.key"], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
        p = subprocess.run(['cp', ksk_private, f"{key_prefix}{ksk_suffix}.private"], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
        p = subprocess.run(['cp', ksk_public, f"{key_prefix}{ksk_suffix}.key"], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")

        # modify zsk, ksk files with sed
        key_list = [
            f"{key_prefix}{zsk_suffix}.private", 
            f"{key_prefix}{zsk_suffix}.key", 
            f"{key_prefix}{ksk_suffix}.private", 
            f"{key_prefix}{ksk_suffix}.key", 
        ]

        first_number = str(f"{start:06}")
        for i in key_list:
            #cmd = f"sed s/sub000000.sub000000/sub{domain_number}.sub{domain_number}/g -i {i}"
            cmd = f"sed s/sub{first_number}.sub{first_number}/sub{domain_number}.sub{domain_number}/g -i {i}"
            p = subprocess.run(cmd.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
        
        # sign the zone
        cmd_gen_signzone = f"dnssec-signzone -e 20501231000000 -S -o sub{domain_number}.sub{domain_number}.delay.com sub.sub.delay.com{domain_number}.template.db"
        rm_file = f"rm -f ./sub.sub.delay{domain_number}.com.template.db"

        #print(cmd_gen_signzone)
        p3 = subprocess.run(cmd_gen_signzone.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
        #print(p3.stdout)

        # remove files
        file_path = "../bind_config_dnssec/sub.sub.delay.com/records/"
        for key in key_list:
            os.remove(f"{file_path}{key}")
        #os.remove(f"{file_path}/sub.sub.delay.com{domain_number}.template.db")

### END: sub[6digits].sub[6digits].delay.com

### START: sub[6digits].delay.com

for i in range(start, end):
    domain_number = str(f"{i:06}")
    with open(f'../bind_config_dnssec/sub.example.com/records/sub{domain_number}.delay.com.template.db', 'w') as f:
        conf_string = """
$TTL 1
@ IN SOA ns01 ns01 (
2010062303
1h
15m
30d
1h )
  IN NS ns01
  IN NS ns02

ns01 IN A 192.168.55.28 
ns02 IN A 192.168.55.29
ns01 IN AAAA 2001:db8:1::28
ns02 IN AAAA 2001:db8:1::29
"""
        f.write(conf_string)

# delegation for sub.delay.com
for i in range(start, end):
    domain_number = str(f"{i:06}")
    with open(f'../bind_config_dnssec/sub.example.com/records/sub{domain_number}.delay.com.template.db', 'a') as f:
        conf_string = f"""
{zone_prefix}{domain_number} IN NS ns01.{zone_prefix}{domain_number}
{zone_prefix}{domain_number} IN NS ns02.{zone_prefix}{domain_number}
ns01.{zone_prefix}{domain_number} IN A 192.168.55.61
ns02.{zone_prefix}{domain_number} IN A 192.168.55.62
ns01.{zone_prefix}{domain_number} IN AAAA 2001:db8:1::61
ns02.{zone_prefix}{domain_number} IN AAAA 2001:db8:1::62
"""
        f.write(conf_string)

# add DS records in its parent zone
for i in range(start, end):
    domain_number = str(f"{i:06}")
    with open(f'../bind_config_dnssec/sub.sub.delay.com/records/dsset-sub{domain_number}.sub{domain_number}.delay.com.', 'r') as f1:
        for dsset in f1.readlines():
            with open(f'../bind_config_dnssec/sub.example.com/records/sub{domain_number}.delay.com.template.db', 'a') as f2:
                f2.write(dsset)

for i in range(start, end):
    domain_number = str(f"{i:06}")

    if i == start:
        cmd_gen_zsk = f"dnssec-keygen -a RSASHA256 -b 1024 sub{domain_number}.delay.com"
        cmd_gen_ksk = f"dnssec-keygen -a RSASHA256 -b 2048 -f KSK sub{domain_number}.delay.com"
        cmd_gen_signzone = f"dnssec-signzone -e 20501231000000 -S -o sub{domain_number}.delay.com sub{domain_number}.delay.com.template.db"
        rm_file = f"rm -f ./sub{domain_number}.delay.com.template.db"

        #print(f"domain : sub{domain_number}.delay.com")
        # zsk
        p1 = subprocess.run(cmd_gen_zsk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
        zsk_suffix = str(p1.stdout).strip().replace(f"Ksub{domain_number}.delay.com.", '')
        zsk_public = str(p1.stdout).strip() + ".key"
        zsk_private = str(p1.stdout).strip() + ".private"
        
        # ksk
        p2 = subprocess.run(cmd_gen_ksk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
        ksk_suffix = str(p2.stdout).strip().replace(f"Ksub{domain_number}.delay.com.", '')
        ksk_public = str(p2.stdout).strip() + ".key"
        ksk_private = str(p2.stdout).strip() + ".private"
        
        # sing the zone
        #print(f"print cmd {cmd_gen_signzone}")
        p3 = subprocess.run(cmd_gen_signzone.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
        #p = subprocess.run(rm_file.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")

    else:
        key_prefix = f"Ksub{domain_number}.delay.com."
        
        # copy zsk, ksk files
        p = subprocess.run(['cp', zsk_private, f"{key_prefix}{zsk_suffix}.private"], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
        p = subprocess.run(['cp', zsk_public, f"{key_prefix}{zsk_suffix}.key"], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
        p = subprocess.run(['cp', ksk_private, f"{key_prefix}{ksk_suffix}.private"], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
        p = subprocess.run(['cp', ksk_public, f"{key_prefix}{ksk_suffix}.key"], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")

        # modify zsk, ksk files with sed
        key_list = [
            f"{key_prefix}{zsk_suffix}.private", 
            f"{key_prefix}{zsk_suffix}.key", 
            f"{key_prefix}{ksk_suffix}.private", 
            f"{key_prefix}{ksk_suffix}.key", 
        ]

        first_number = str(f"{start:06}")
        for i in key_list:
            cmd = f"sed s/sub{first_number}/sub{domain_number}/g -i {i}"
            p = subprocess.run(cmd.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
        
        # sign the zone
        cmd_gen_signzone = f"dnssec-signzone -e 20501231000000 -S -o sub{domain_number}.delay.com sub{domain_number}.delay.com.template.db"
        rm_file = f"rm -f ./sub.example{domain_number}.com.template.db"

        #print(cmd_gen_signzone)
        p3 = subprocess.run(cmd_gen_signzone.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
        #print(p3.stdout, p3.stderr)

        # remove files
        file_path = "../bind_config_dnssec/sub.example.com/records/"
        for key in key_list:
            os.remove(f"{file_path}{key}")
        #os.remove(f"{file_path}/sub.sub.example.com{domain_number}.template.db")

### END: sub[6digits].delay.com
