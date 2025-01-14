#!/bin/sh

rm -rf ../bind_config_dnssec/sub.sub.example.com/records
mkdir ../bind_config_dnssec/sub.sub.example.com/records
cp ./named.ca ../bind_config_dnssec/sub.sub.example.com/records

rm -rf ../bind_config_dnssec/sub.sub.delay.com/records
mkdir ../bind_config_dnssec/sub.sub.delay.com/records
cp ./named.ca ../bind_config_dnssec/sub.sub.delay.com/records

tree -if ../bind_config_dnssec/sub.sub.example.com/ |egrep 'named.conf' | xargs -I{} rm -rf {}
tree -if ../bind_config_dnssec/sub.sub.delay.com/ |egrep 'named.conf' | xargs -I{} rm -rf {}

rm -rf ../bind_config_dnssec/sub.example.com/records
mkdir ../bind_config_dnssec/sub.example.com/records
cp ./named.ca ../bind_config_dnssec/sub.example.com/records


rm -rf ../bind_config_dnssec/example.com/records
mkdir ../bind_config_dnssec/example.com/records
cp ./named.ca ../bind_config_dnssec/example.com/records

tree -if ../bind_config_dnssec/example.com/ |egrep 'named.conf' | xargs -I{} rm -rf {}

rm -rf ../bind_config_dnssec/com/records
mkdir ../bind_config_dnssec/com/records
cp ./named.ca ../bind_config_dnssec/com/records

tree -if ../bind_config_dnssec/com/ |egrep 'named.conf' | xargs -I{} rm -rf {}
tree -if ../bind_config_dnssec/root/ |egrep 'named.conf' | xargs -I{} rm -rf {}
tree -if ../bind_config_dnssec/root/records |egrep 'dsset|signed|key|private|root.db' | xargs -I{} rm -rf {}
