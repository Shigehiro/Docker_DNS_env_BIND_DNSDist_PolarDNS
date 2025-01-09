#!/usr/bin/env python3

zone_prefix = 'sub'
zone_suffix = 'example.com'
zone_suffix_polardns = 'broken.com'
zone_suffix_delay = 'delay.com'
number_of_zone = 10

# Generate zone file for example.com
with open('../bind_config/example.com/records/example.com.template.db', 'w') as f:
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

ns01 IN A 192.168.55.24 ; authority of example.com
ns02 IN A 192.168.55.25 ; authority of example.com
ns01 IN AAAA 2001:db8:1::24 ; authority of example.com
ns02 IN AAAA 2001:db8:1::25 ; authority of example.com
"""
    f.write(conf_string)

# delegation for sub.example.com
with open('../bind_config/example.com/records/example.com.template.db', 'a') as f:
    for i in range(0,number_of_zone):
        domain_number = str(f"{i:06}")
        conf_string = f"""
{zone_prefix}{domain_number}.{zone_suffix}. IN NS ns01.{zone_prefix}{domain_number}.{zone_suffix}.
{zone_prefix}{domain_number}.{zone_suffix}. IN NS ns02.{zone_prefix}{domain_number}.{zone_suffix}.
ns01.{zone_prefix}{domain_number}.{zone_suffix}. IN A 192.168.55.28 ; authority of {zone_prefix}{domain_number}.{zone_suffix}.
ns02.{zone_prefix}{domain_number}.{zone_suffix}. IN A 192.168.55.29 ; authority of {zone_prefix}{domain_number}.{zone_suffix}.
ns01.{zone_prefix}{domain_number}.{zone_suffix}. IN AAAA 2001:db8:1::28 ; authority of {zone_prefix}{domain_number}.{zone_suffix}.
ns02.{zone_prefix}{domain_number}.{zone_suffix}. IN AAAA 2001:db8:1::29 ; authority of {zone_prefix}{domain_number}.{zone_suffix}.
"""
        f.write(conf_string)

# Generate zone file for broken.com
with open('../bind_config/example.com/records/broken.com.template.db', 'w') as f:
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

ns01 IN A 192.168.55.24 ; authority of broken.com
ns02 IN A 192.168.55.25 ; authority of broken.com
ns01 IN AAAA 2001:db8:1::24 ; authority of broken.com
ns02 IN AAAA 2001:db8:1::25 ; authority of broken.com
"""
    f.write(conf_string)

# delegation for sub.broken.com
with open('../bind_config/example.com/records/broken.com.template.db', 'a') as f:
    for i in range(0,number_of_zone):
        domain_number = str(f"{i:06}")
        conf_string = f"""
{zone_prefix}{domain_number}.{zone_suffix_polardns}. IN NS ns01.{zone_prefix}{domain_number}.{zone_suffix_polardns}.
{zone_prefix}{domain_number}.{zone_suffix_polardns}. IN NS ns02.{zone_prefix}{domain_number}.{zone_suffix_polardns}.
ns01.{zone_prefix}{domain_number}.{zone_suffix_polardns}. IN A 192.168.55.28 ; authority of {zone_prefix}{domain_number}.{zone_suffix_polardns}.
ns02.{zone_prefix}{domain_number}.{zone_suffix_polardns}. IN A 192.168.55.29 ; authority of {zone_prefix}{domain_number}.{zone_suffix_polardns}.
ns01.{zone_prefix}{domain_number}.{zone_suffix_polardns}. IN AAAA 2001:db8:1::28 ; authority of {zone_prefix}{domain_number}.{zone_suffix_polardns}.
ns02.{zone_prefix}{domain_number}.{zone_suffix_polardns}. IN AAAA 2001:db8:1::29 ; authority of {zone_prefix}{domain_number}.{zone_suffix_polardns}.
"""
        f.write(conf_string)

# Generate zone file for delay.com
with open('../bind_config/example.com/records/delay.com.template.db', 'w') as f:
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

ns01 IN A 192.168.55.24 ; authority of delay.com
ns02 IN A 192.168.55.25 ; authority of delay.com
ns01 IN AAAA 2001:db8:1::24 ; authority of delay.com
ns02 IN AAAA 2001:db8:1::25 ; authority of delay.com
"""
    f.write(conf_string)

# delegation for sub.delay.com
with open('../bind_config/example.com/records/delay.com.template.db', 'a') as f:
    for i in range(0,number_of_zone):
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

# Generate named.conf
with open('../bind_config/example.com/config/named.conf', 'w') as f:
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
  file "/var/lib/bind/example.com.template.db";
}};
"""
    f.write(conf_string)

    conf_string = f"""
zone "{zone_suffix_polardns}" in {{
  type master;
  file "/var/lib/bind/broken.com.template.db";
}};
"""
    f.write(conf_string)

    conf_string = f"""
zone "{zone_suffix_delay}" in {{
  type master;
  file "/var/lib/bind/delay.com.template.db";
}};
"""
    f.write(conf_string)

print("restart the containers to reflect the config")
