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

# delay.com
with open('../bind_config_dnssec/example.com/records/delay.com.template.db', 'w') as f:
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

ns01 IN A 192.168.55.24 ; authority of delay.com
ns02 IN A 192.168.55.25 ; authority of delay.com
ns01 IN AAAA 2001:db8:1::24 ; authority of delay.com
ns02 IN AAAA 2001:db8:1::25 ; authority of delay.com
"""
    f.write(conf_string)

# delegation for sub.delay.com
with open('../bind_config_dnssec/example.com/records/delay.com.template.db', 'a') as f:
    for i in range(start, end):
        domain_number = str(f"{i:06}")
        conf_string = f"""
{zone_prefix}{domain_number}.{zone_suffix_delay}. IN NS ns01.{zone_prefix}{domain_number}.{zone_suffix_delay}.
{zone_prefix}{domain_number}.{zone_suffix_delay}. IN NS ns02.{zone_prefix}{domain_number}.{zone_suffix_delay}.
ns01.{zone_prefix}{domain_number}.{zone_suffix_delay}. IN A 192.168.55.28 ; authority of {zone_prefix}{domain_number}.{zone_suffix_delay}.
ns02.{zone_prefix}{domain_number}.{zone_suffix_delay}. IN A 192.168.55.29 ; authority of {zone_prefix}{domain_number}.{zone_suffix_delay}.
ns01.{zone_prefix}{domain_number}.{zone_suffix_delay}. IN AAAA 2001:db8:1::28 ; authority of {zone_prefix}{domain_number}.{zone_suffix_delay}.
ns02.{zone_prefix}{domain_number}.{zone_suffix_delay}. IN AAAA 2001:db8:1::29 ; authority of {zone_prefix}{domain_number}.{zone_suffix_delay}.
"""
        f.write(conf_string)

# add DS records in its parent zone
for i in range(start, end):
    domain_number = str(f"{i:06}")
    with open(f'../bind_config_dnssec/sub.example.com/records/dsset-sub{domain_number}.delay.com.', 'r') as f1:
        for dsset in f1.readlines():
            with open('../bind_config_dnssec/example.com/records/delay.com.template.db', 'a') as f2:
                f2.write(dsset)

# sign the zone
cmd_gen_zsk = f"dnssec-keygen -a RSASHA256 -b 1024 delay.com"
cmd_gen_ksk = f"dnssec-keygen -a RSASHA256 -b 2048 -f KSK delay.com"
cmd_gen_signzone = f"dnssec-signzone -e 20501231000000 -S -o delay.com delay.com.template.db"

# zsk
p1 = subprocess.run(cmd_gen_zsk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/example.com/records")

# ksk
p2 = subprocess.run(cmd_gen_ksk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/example.com/records")

# sing the zone
p3 = subprocess.run(cmd_gen_signzone.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/example.com/records")

### END : eaxmple.com, delay.com
