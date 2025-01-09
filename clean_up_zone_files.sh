#!/bin/sh

tree -if ./bind_config_dnssec/sub.sub.example.com/records/ |egrep 'template|.key|.private' | xargs -I{} rm {}
tree -if ./bind_config_dnssec/sub.sub.delay.com/records/ |egrep 'template|.key|.private' | xargs -I{} rm {}
tree -if ./bind_config_dnssec/sub.example.com/records/ |egrep 'template|.key|.private' | xargs -I{} rm {}
tree -if ./bind_config_dnssec/sub.delay.com/records/ |egrep 'template|.key|.private' | xargs -I{} rm {}
