# Set up internal DNS servers with BIND, dnsdist and PolarDNS

- [Set up internal DNS servers with BIND, dnsdist and PolarDNS](#set-up-internal-dns-servers-with-bind-dnsdist-and-polardns)
  - [Description](#description)
  - [Genrate config](#genrate-config)
  - [Dig samples against PolarDNS (broken.com)](#dig-samples-against-polardns-brokencom)
  - [Add latency on the dnsdist](#add-latency-on-the-dnsdist)
  - [Set up DNSSEC environment](#set-up-dnssec-environment)

## Description

Set up internal DNS servers with docker compose for DNS testing.

- root * 2 (BIND * 2)
- com * 2 (BIND * 2)
  - dnsdist is in front of them.
- example.com * 4 (BIND * 4)
  - dnsdist is in front of them.
- sub[000000-099999].[example|broken].com * 4 (BIND * 4)
  - dnsdist is in front of them
- sub[000000-099999].sub[000000-099999].example.com * 4 (BIND * 4)
  - dnsdist is in front of them
- sub[000000-099999].sub[000000-099999].broken.com * 4 (PolarDNS * 4)
  - PolarDNS handles queries. this domain is useful to test broken responses.

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
addAction(AllRule(), DelayAction(100))
```

## Set up DNSSEC environment

```
$ cd Python_gen_zone_conf_DNSSEC/
```

Edit gen_script.py as you like.
```
$ grep -E '^start|^end|^step' gen_script.py
start = 0
end = 300000
step = 50000
```

In the above case, a total of **600,000 zones** will be generated, ranging from **sub000000.sub000000.example|delay.com** to **sub299999.sub299999.example|delay.com**, with secured zones.<br>
Run the script.
```
$ ./gen_script.py
```

The python script will generate three shell scipts as below.
```
$ ls *0[1-3]*.sh
gen_dnssec_conf_01.sh  gen_dnssec_conf_02.sh  gen_dnssec_conf_03.sh
```

Run the first script and wait until the script completes.  
This script spawns some processes in the background, so make sure the processes have completed using `ps` or another similar tool.
```
./gen_dnssec_conf_01.sh
```

Run the second and, lastly the third script and start the containers.
```
./gen_dnssec_conf_02.sh
```

```
./gen_dnssec_conf_03.sh
```

```
cd ..
docker compose -f dnssec_host_net_compose.yml up -d
```

Add the key on a full resolver so that the server can validate queries.
```
$ grep '257 3 8' bind_config_dnssec/root/records/*.key
```