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

### START: sub[6digits].sub[6digits].example.com

# Generate named.conf
with open('../bind_config_dnssec/sub.sub.example.com/config/named.conf', 'w') as f:
    conf_string = """
options {
  directory "/var/cache/bind";
  dnssec-validation false;
  allow-query { any; };
  recursion no;
  allow-recursion { none; };
  listen-on { any; };
  listen-on-v6 { any; };
  notify no;
};

zone  "." in {
        type hint;
        file "/var/lib/bind/named.ca";
        };
"""
    f.write(conf_string)

# Generate named.conf for sub.sub.example.com
with open('../bind_config_dnssec/sub.sub.example.com/config/named.conf', 'a') as f:
    for i in range(start, end):
        domain_number = str(f"{i:06}")
        name_conf_string = f"""
zone "sub{domain_number}.sub{domain_number}.{zone_suffix}" in {{
  type master;
  file "/var/lib/bind/sub.sub.example.com{domain_number}.template.db.signed";
}};
"""
        f.write(name_conf_string)

### END: sub[6digits].sub[6digits].example.com

### START: sub[6digits].sub[6digits].delay.com

# Generate named.conf
with open('../bind_config_dnssec/sub.sub.delay.com/config/named.conf', 'w') as f:
    conf_string = """
options {
  directory "/var/cache/bind";
  dnssec-validation false;
  allow-query { any; };
  recursion no;
  allow-recursion { none; };
  listen-on { any; };
  listen-on-v6 { any; };
  notify no;
};

zone  "." in {
        type hint;
        file "/var/lib/bind/named.ca";
        };
"""
    f.write(conf_string)

# Generate named.conf for sub.sub.delay.com
with open('../bind_config_dnssec/sub.sub.delay.com/config/named.conf', 'a') as f:
    for i in range(start, end):
        domain_number = str(f"{i:06}")
        name_conf_string = f"""
zone "sub{domain_number}.sub{domain_number}.{zone_suffix_delay}" in {{
  type master;
  file "/var/lib/bind/sub.sub.delay.com{domain_number}.template.db.signed";
}};
"""
        f.write(name_conf_string)

### END: sub[6digits].sub[6digits].delay.com

### START: sub[6digits].example.com

# Generate named.conf for sub[6digits].example.com and sub[6digits].delay.com

with open('../bind_config_dnssec/sub.example.com/config/named.conf', 'w') as f:
    conf_string = """
options {
  directory "/var/cache/bind";
  dnssec-validation false;
  allow-query { any; };
  recursion no;
  allow-recursion { none; };
  listen-on { any; };
  listen-on-v6 { any; };
  notify no;
};

zone  "." in {
        type hint;
        file "/var/lib/bind/named.ca";
        };
"""
    f.write(conf_string)
    
# Generate named.conf for sub[6digits].example.com

for i in range(start, end):
    domain_number = str(f"{i:06}")
    with open('../bind_config_dnssec/sub.example.com/config/named.conf', 'a') as f:
        conf_string = f"""
zone "{zone_prefix}{domain_number}.{zone_suffix}" in {{
  type master;
  file "/var/lib/bind/sub{domain_number}.example.com.template.db.signed";
}};
"""
        f.write(conf_string)

### END: sub[6digits].example.com

### START: sub[6digits].delay.com

# Generate named.conf for sub[6digits].example.com

for i in range(start, end):
    domain_number = str(f"{i:06}")
    with open('../bind_config_dnssec/sub.example.com/config/named.conf', 'a') as f:
        conf_string = f"""
zone "{zone_prefix}{domain_number}.{zone_suffix_delay}" in {{
  type master;
  file "/var/lib/bind/sub{domain_number}.delay.com.template.db.signed";
}};
"""
        f.write(conf_string)

### END: sub[6digits].delay.com

### START : eaxmple.com, delay.com

# Generate named.conf
with open('../bind_config_dnssec/example.com/config/named.conf', 'w') as f:
    conf_string = """
options {
  directory "/var/cache/bind";
  dnssec-validation false;
  allow-query { any; };
  recursion no;
  allow-recursion { none; };
  listen-on { any; };
  listen-on-v6 { any; };
  notify no;
};

zone  "." in {
        type hint;
        file "/var/lib/bind/named.ca";
        };
"""
    f.write(conf_string)

    conf_string = f"""
zone "{zone_suffix}" in {{
  type master;
  file "/var/lib/bind/example.com.template.db.signed";
}};
"""
    f.write(conf_string)

    conf_string = f"""
zone "{zone_suffix_delay}" in {{
  type master;
  file "/var/lib/bind/delay.com.template.db.signed";
}};
"""
    f.write(conf_string)

### END : eaxmple.com, delay.com

### START : com

# com
with open('../bind_config_dnssec/com/records/com.db', 'w') as f:
    conf_string = """
$TTL 3600
@ IN SOA ns01 ns01 (
2010062303
1h
15m
30d
1h )
  IN NS ns01
  IN NS ns02

ns01 IN A 192.168.55.22
ns01 IN AAAA 2001:db8:1::22
ns02 IN A 192.168.55.23
ns02 IN AAAA 2001:db8:1::23

example IN NS ns01.example
example IN NS ns02.example
ns01.example IN A 192.168.55.24
ns02.example IN A 192.168.55.25
ns01.example IN AAAA 2001:db8:1::24
ns02.example IN AAAA 2001:db8:1::25

broken IN NS ns01.broken
broken IN NS ns02.broken
ns01.broken IN A 192.168.55.24
ns02.broken IN A 192.168.55.25
ns01.broken IN AAAA 2001:db8:1::24
ns02.broken IN AAAA 2001:db8:1::25

delay IN NS ns01.delay
delay IN NS ns02.delay
ns01.delay IN A 192.168.55.24
ns02.delay IN A 192.168.55.25
ns01.delay IN AAAA 2001:db8:1::24
ns02.delay IN AAAA 2001:db8:1::25
"""
    f.write(conf_string)

# add DS records in its parent zone. example.com
for i in range(0,1):
    # example.com
    domain_number = str(f"{i:06}")
    with open(f'../bind_config_dnssec/example.com/records/dsset-example.com.', 'r') as f1:
        for dsset in f1.readlines():
            with open('../bind_config_dnssec/com/records/com.db', 'a') as f2:
                f2.write(dsset)
# add DS records in its parent zone. delay.com
for i in range(0,1):
    domain_number = str(f"{i:06}")
    with open(f'../bind_config_dnssec/example.com/records/dsset-delay.com.', 'r') as f1:
        for dsset in f1.readlines():
            with open('../bind_config_dnssec/com/records/com.db', 'a') as f2:
                f2.write(dsset)

# sign the zone
cmd_gen_zsk = f"dnssec-keygen -a RSASHA256 -b 1024 com"
cmd_gen_ksk = f"dnssec-keygen -a RSASHA256 -b 2048 -f KSK com"
cmd_gen_signzone = f"dnssec-signzone -e 20501231000000 -S -o com com.db"

# zsk
p1 = subprocess.run(cmd_gen_zsk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/com/records")

# ksk
p2 = subprocess.run(cmd_gen_ksk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/com/records")

# sing the zone
p3 = subprocess.run(cmd_gen_signzone.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/com/records")

# named.conf for com
with open('../bind_config_dnssec/com/config/named.conf', 'w') as f:
    conf_string = """
options {
  directory "/var/cache/bind";
  dnssec-validation false;
  allow-query { any; };
  recursion no;
  allow-recursion { none; };
  listen-on { any; };
  listen-on-v6 { any; };
  notify no;
};
zone  "." in {
        type hint;
        file "/var/lib/bind/named.ca";
        };
zone "com" in {
  type master;
  file "/var/lib/bind/com.db.signed";
};
"""
    f.write(conf_string)

### END : com

### START : .

# get ds record of com
dsset_com = str()
with open('../bind_config_dnssec/com/records/dsset-com.', 'r') as f:
    for line in f.readlines():
        dsset_com = line
        
# generate zone file for .
with open('../bind_config_dnssec/root/records/root.db', 'w') as f:
    conf_string = f"""
$ORIGIN .
$TTL 864000
. IN SOA x.root-servers.net. hostmaster.root-servers.net. (
2010062304
1h
15m
30d
1h )
  IN NS x.root-servers.net.
  IN NS y.root-servers.net.

x.root-servers.net. IN A 192.168.55.20
x.root-servers.net. IN AAAA 2001:db8:1::20
y.root-servers.net. IN A 192.168.55.21
y.root-servers.net. IN AAAA 2001:db8:1::21

com. IN NS ns01.com.
com. IN NS ns02.com.
ns01.com. IN A 192.168.55.22
ns01.com. IN AAAA 2001:db8:1::22
ns02.com. IN A 192.168.55.23
ns02.com. IN AAAA 2001:db8:1::23
{dsset_com}
"""
    f.write(conf_string)

# sign the zone
cmd_gen_zsk = f"dnssec-keygen -a RSASHA256 -b 1024 ."
cmd_gen_ksk = f"dnssec-keygen -a RSASHA256 -b 2048 -f KSK ."
cmd_gen_signzone = f"dnssec-signzone -e 20501231000000 -S -o . root.db"

# zsk
p1 = subprocess.run(cmd_gen_zsk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/root/records")

# ksk
p2 = subprocess.run(cmd_gen_ksk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/root/records")

# sing the zone
p3 = subprocess.run(cmd_gen_signzone.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/root/records")

# generate named.conf for .
with open('../bind_config_dnssec/root/config/named.conf', 'w') as f:
    conf_string = """
options {
  directory "/var/cache/bind";
  dnssec-validation false;
  allow-query { any; };
  recursion no;
  allow-recursion { none; };
  listen-on { any; };
  listen-on-v6 { any; };
  notify no;
};

zone  "." in {
        type master;
        file "/var/lib/bind/root.db.signed";
        };
"""
    f.write(conf_string)

### START : remove unwanted files

rm_cmd = [
"tree -if ../bind_config_dnssec/com/records/ |grep -E 'dsset|com.db|.key|.private' | grep -v signed | xargs -I{} rm {}",
"tree -if ../bind_config_dnssec/root/records/ |grep -E 'root.db' | grep -v signed | xargs -I{} rm {}",
]

for i in rm_cmd:
    os.system(i)

### END : remove unwanted files