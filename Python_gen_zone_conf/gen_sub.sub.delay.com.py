#!/usr/bin/env python3

zone_suffix = 'delay.com'
number_of_zone = 10

# Generate zone file for sub.delay.com
with open('../bind_config/sub.sub.delay.com/records/sub.sub.delay.com.template.db', 'w') as f:
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
with open('../bind_config/sub.sub.delay.com/config/named.conf', 'w') as f:
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
with open('../bind_config/sub.sub.delay.com/config/named.conf', 'a') as f:
    for i in range(0,number_of_zone):
        domain_number = str(f"{i:06}")
        name_conf_string = f"""
zone "sub{domain_number}.sub{domain_number}.{zone_suffix}" in {{
  type master;
  file "/var/lib/bind/sub.sub.delay.com.template.db";
}};
"""
        f.write(name_conf_string)

print("restart the containers to reflect the config")
