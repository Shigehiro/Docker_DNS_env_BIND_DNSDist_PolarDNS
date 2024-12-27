#!/usr/bin/env python3

zone_prefix = 'sub'
zone_suffix = 'example.com'
zone_suffix_polardns = 'broken.com'
number_of_zone = 100000

# Generate zone file for sub.example.com
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

# Generate zone file for sub.broken.com
for i in range(0,number_of_zone):
    domain_number = str(f"{i:06}")
    with open(f'../bind_config/sub.example.com/records/sub{domain_number}.broken.com.template.db', 'w') as f:
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

ns01 IN A 192.168.55.28
ns02 IN A 192.168.55.29
ns01 IN AAAA 2001:db8:1::28
ns02 IN AAAA 2001:db8:1::29
"""
        f.write(conf_string)

# delegation for sub.broken.com
for i in range(0,number_of_zone):
    domain_number = str(f"{i:06}")
    with open(f'../bind_config/sub.example.com/records/sub{domain_number}.broken.com.template.db', 'a') as f:
        conf_string = f"""
{zone_prefix}{domain_number} IN NS ns01.{zone_prefix}{domain_number}
{zone_prefix}{domain_number} IN NS ns02.{zone_prefix}{domain_number}
{zone_prefix}{domain_number} IN NS ns03.{zone_prefix}{domain_number}
{zone_prefix}{domain_number} IN NS ns04.{zone_prefix}{domain_number}
ns01.{zone_prefix}{domain_number} IN A 192.168.55.49
ns02.{zone_prefix}{domain_number} IN A 192.168.55.50
ns03.{zone_prefix}{domain_number} IN A 192.168.55.51
ns04.{zone_prefix}{domain_number} IN A 192.168.55.52
ns01.{zone_prefix}{domain_number} IN AAAA 2001:db8:1::49
ns02.{zone_prefix}{domain_number} IN AAAA 2001:db8:1::50
ns03.{zone_prefix}{domain_number} IN AAAA 2001:db8:1::51
ns04.{zone_prefix}{domain_number} IN AAAA 2001:db8:1::52
"""
        f.write(conf_string)

# Generate named.conf
with open('../bind_config/sub.example.com/config/named.conf', 'w') as f:
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

# Generate named.conf for sub.example.com
for i in range(0,number_of_zone):
    domain_number = str(f"{i:06}")
    with open('../bind_config/sub.example.com/config/named.conf', 'a') as f:
        conf_string = f"""
zone "{zone_prefix}{domain_number}.{zone_suffix}" in {{
  type master;
  file "/var/lib/bind/sub{domain_number}.example.com.template.db";
}};
"""
        f.write(conf_string)

# Generate named.conf for sub.broken.com
for i in range(0,number_of_zone):
    domain_number = str(f"{i:06}")
    with open('../bind_config/sub.example.com/config/named.conf', 'a') as f:
        conf_string = f"""
zone "{zone_prefix}{domain_number}.{zone_suffix_polardns}" in {{
  type master;
  file "/var/lib/bind/sub{domain_number}.broken.com.template.db";
}};
"""
        f.write(conf_string)

print("restart the containers to reflect the config")
