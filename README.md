# Set up internal DNS servers with BIND, dnsdist and PolarDNS

Set up DNS servers with docker compose for the DNS testing.

- root * 2
- com * 2, dnsdist is in front of them.
- example.com * 4, dnsdist is in front of them.
- sub[000000-099999].[example|broken].com * 4, dnsdist is in front of them
- sub[000000-099999].sub[000000-099999].example.com * 4, dnsdist is in front of them
- sub[000000-099999].sub[000000-099999].broken.com * 4, polardns handles queries. this domain is useful to test broken responses.

## Genrate config

```
cd Python_gen_zone_conf/
```

generate named.conf and zone files.
```
./gen_example.com.py
./gen_sub.example.com.py
./gen_sub.sub.example.com.py
```

## Dig samples against PolarDNS (broken.com)

If you would like to know the detail, see [PolarDNS doc](https://github.com/oryxlabs/PolarDNS/tree/main)
```
dig @127.1 always.sub000000.sub000000.broken.com 

dig @127.1 size.512.sub000000.sub000000.broken.com 

dig @127.1 always.slp300.sub000000.sub000000.broken.com

dig @127.1 always.ttl300000.slp300.sub000000.sub000000.broken.com  

dig @127.1 size.512.slp500.sub000000.sub000000.broken.com 

dig @127.1 bigtxt.100.20.slp500.sub000000.sub000000.broken.com txt

dig @127.1 always.tc.sub000000.sub000000.broken.com

dig @127.1 size.128.cut16.sub000000.sub000000.broken.com
```

## Add latency on the dnsdist

You can add the delay with DelayAction.<br>
Edit dnsdist.conf and restart the dnsdist container to reflect that.
```
$ grep -i delay bind_config/dnsdist/dnsdist_com.conf
-- If you would like to add the delay, enable the below
-- addAction(AllRule(), DelayAction(100))
```