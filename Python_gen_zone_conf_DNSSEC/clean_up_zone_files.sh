#!/bin/sh

tree -if ../bind_config_dnssec/sub.sub.example.com/records/ |egrep 'dsset|template|.key|.private' | xargs -I{} rm {}
tree -if ../bind_config_dnssec/sub.sub.delay.com/records/ |egrep 'dsset|template|.key|.private' | xargs -I{} rm {}
tree -if ../bind_config_dnssec/sub.sub.example.com/ |egrep 'named.conf' | xargs -I{} rm -rf {}
tree -if ../bind_config_dnssec/sub.sub.delay.com/ |egrep 'named.conf' | xargs -I{} rm -rf {}
tree -if ../bind_config_dnssec/sub.delay.com/records/ |egrep 'dsset|template|.key|.private' | xargs -I{} rm {}
tree -if ../bind_config_dnssec/sub.example.com/ |egrep 'named.conf' | xargs -I{} rm -rf {}
tree -if ../bind_config_dnssec/sub.delay.com/ |egrep 'named.conf' | xargs -I{} rm -rf {}
tree -if ../bind_config_dnssec/example.com/records/ |egrep 'dsset|template|.key|.private' | xargs -I{} rm {}
tree -if ../bind_config_dnssec/example.com/ |egrep 'named.conf' | xargs -I{} rm -rf {}
tree -if ../bind_config_dnssec/com/records/ |egrep 'dsset|template|.key|.private' | xargs -I{} rm {}
tree -if ../bind_config_dnssec/com/ |egrep 'named.conf' | xargs -I{} rm -rf {}
tree -if ../bind_config_dnssec/root/ |egrep 'named.conf' | xargs -I{} rm -rf {}
