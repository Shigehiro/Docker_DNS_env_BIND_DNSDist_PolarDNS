#!/usr/bin/env python3

#from subprocess import check_output
import subprocess

zone_prefix = 'sub'
zone_suffix = 'example.com'
zone_suffix_delay = 'delay.com'
number_of_zone = 3

### START: sub[6digits].sub[6digits].example.com

# Generate zone file for sub.example.com
for i in range(0,number_of_zone):
    domain_number = str(f"{i:06}")
    with open(f'../bind_config_dnssec/sub.sub.example.com/records/sub.sub.example.com{domain_number}.template.db', 'w') as f:
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

ns01 IN A 192.168.55.59
ns02 IN A 192.168.55.60
ns01 IN AAAA 2001:db8:1::59
ns02 IN AAAA 2001:db8:1::60
* 86400 IN A 127.0.0.1
* 86400 IN AAAA ::1
* 86400 IN TXT 'hello'
"""
        f.write(conf_string)

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
    for i in range(0,number_of_zone):
        domain_number = str(f"{i:06}")
        name_conf_string = f"""
zone "sub{domain_number}.sub{domain_number}.{zone_suffix}" in {{
  type master;
  file "/var/lib/bind/sub.sub.example.com{domain_number}.template.db.signed";
}};
"""
        f.write(name_conf_string)

#print("sign the zone")

for i in range(0,number_of_zone):
    domain_number = str(f"{i:06}")
    cmd_gen_zsk = f"dnssec-keygen -a RSASHA256 -b 1024 sub{domain_number}.sub{domain_number}.example.com"
    cmd_gen_ksk = f"dnssec-keygen -a RSASHA256 -b 2048 -f KSK sub{domain_number}.sub{domain_number}.example.com"
    cmd_gen_signzone = f"dnssec-signzone -e 20501231000000 -S -o sub{domain_number}.sub{domain_number}.example.com sub.sub.example.com{domain_number}.template.db"
    rm_file = f"rm -f ./sub.sub.example{domain_number}.com.template.db"

    #print(f"domain : sub{domain_number}.sub{domain_number}.example.com")
    # zsk
    p1 = subprocess.run(cmd_gen_zsk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.example.com/records")
    #print(p1.stdout)
    zsk_private = f"{p1.stdout}.private"
    zsk_public = f"{p1.stdout}.key"

    # ksk
    p2 = subprocess.run(cmd_gen_ksk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.example.com/records")
    #print(p2.stdout)
    ksk_private = f"{p2.stdout}.private"
    ksk_public = f"{p2.stdout}.key"

    # sing the zone
    #print(f"print cmd {cmd_gen_signzone}")
    p3 = subprocess.run(cmd_gen_signzone.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.example.com/records")
    
    p = subprocess.run(rm_file.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.example.com/records")
    p = subprocess.run(['rm','-f', zsk_private], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.example.com/records")
    p = subprocess.run(['rm','-f', zsk_public], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.example.com/records")
    p = subprocess.run(['rm','-f', ksk_private], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.example.com/records")
    p = subprocess.run(['rm','-f', ksk_public], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.example.com/records")

### END: sub[6digits].sub[6digits].example.com

### START: sub[6digits].sub[6digits].delay.com

# Generate zone file for sub.delay.com
for i in range(0,number_of_zone):
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
    for i in range(0,number_of_zone):
        domain_number = str(f"{i:06}")
        name_conf_string = f"""
zone "sub{domain_number}.sub{domain_number}.{zone_suffix_delay}" in {{
  type master;
  file "/var/lib/bind/sub.sub.delay.com{domain_number}.template.db.signed";
}};
"""
        f.write(name_conf_string)

#print("sign the zone")

for i in range(0,number_of_zone):
    domain_number = str(f"{i:06}")
    cmd_gen_zsk = f"dnssec-keygen -a RSASHA256 -b 1024 sub{domain_number}.sub{domain_number}.delay.com"
    cmd_gen_ksk = f"dnssec-keygen -a RSASHA256 -b 2048 -f KSK sub{domain_number}.sub{domain_number}.delay.com"
    cmd_gen_signzone = f"dnssec-signzone -e 20501231000000 -S -o sub{domain_number}.sub{domain_number}.delay.com sub.sub.delay.com{domain_number}.template.db"
    rm_file = f"rm -f ./sub.sub.delay{domain_number}.com.template.db"

    #print(f"domain : sub{domain_number}.sub{domain_number}.delay.com")
    # zsk
    p1 = subprocess.run(cmd_gen_zsk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
    #print(p1.stdout)
    zsk_private = f"{p1.stdout}.private"
    zsk_public = f"{p1.stdout}.key"

    # ksk
    p2 = subprocess.run(cmd_gen_ksk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
    #print(p2.stdout)
    ksk_private = f"{p2.stdout}.private"
    ksk_public = f"{p2.stdout}.key"

    # sing the zone
    #print(f"print cmd {cmd_gen_signzone}")
    p3 = subprocess.run(cmd_gen_signzone.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
    
    p = subprocess.run(rm_file.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
    p = subprocess.run(['rm','-f', zsk_private], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
    p = subprocess.run(['rm','-f', zsk_public], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
    p = subprocess.run(['rm','-f', ksk_private], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")
    p = subprocess.run(['rm','-f', ksk_public], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.sub.delay.com/records")

### END: sub[6digits].sub[6digits].delay.com

### START: sub[6digits].example.com

for i in range(0,number_of_zone):
    domain_number = str(f"{i:06}")
    with open(f'../bind_config/sub.example.com/records/sub{domain_number}.example.com.template.db', 'w') as f:
        conf_string = """
$TTL 60
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

# delegation for sub.example.com
for i in range(0,number_of_zone):
    domain_number = str(f"{i:06}")
    with open(f'../bind_config/sub.example.com/records/sub{domain_number}.example.com.template.db', 'a') as f:
        conf_string = f"""
{zone_prefix}{domain_number} IN NS ns01.{zone_prefix}{domain_number}
{zone_prefix}{domain_number} IN NS ns02.{zone_prefix}{domain_number}
ns01.{zone_prefix}{domain_number} IN A 192.168.55.59
ns02.{zone_prefix}{domain_number} IN A 192.168.55.60
ns01.{zone_prefix}{domain_number} IN AAAA 2001:db8:1::59
ns02.{zone_prefix}{domain_number} IN AAAA 2001:db8:1::60
"""
        f.write(conf_string)

#print("sign the zone")

for i in range(0,number_of_zone):
    domain_number = str(f"{i:06}")
    cmd_gen_zsk = f"dnssec-keygen -a RSASHA256 -b 1024 sub{domain_number}.example.com"
    cmd_gen_ksk = f"dnssec-keygen -a RSASHA256 -b 2048 -f KSK sub{domain_number}.example.com"
    cmd_gen_signzone = f"dnssec-signzone -e 20501231000000 -S -o sub{domain_number}.example.com sub{domain_number}.example.com.template.db"
    rm_file = f"rm -f ./sub{domain_number}.example.com.template.db"

    #print(f"domain : sub{domain_number}.example.com")
    # zsk
    p1 = subprocess.run(cmd_gen_zsk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
    #print(p1.stdout)
    zsk_private = f"{p1.stdout}.private"
    zsk_public = f"{p1.stdout}.key"

    # ksk
    p2 = subprocess.run(cmd_gen_ksk.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
    #print(p2.stdout)
    ksk_private = f"{p2.stdout}.private"
    ksk_public = f"{p2.stdout}.key"

    # sing the zone
    #print(f"print cmd {cmd_gen_signzone}")
    p3 = subprocess.run(cmd_gen_signzone.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
    
    p = subprocess.run(rm_file.split(), capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
    p = subprocess.run(['rm','-f', zsk_private], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
    p = subprocess.run(['rm','-f', zsk_public], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
    p = subprocess.run(['rm','-f', ksk_private], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")
    p = subprocess.run(['rm','-f', ksk_public], capture_output=True, text=True, cwd="../bind_config_dnssec/sub.example.com/records")