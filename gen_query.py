#!/usr/bin/env/python3 

zone_suffix = 'example.com'
zone_suffix_polardns = 'broken.com'
number_of_zone = 10

# query list to make hot cache
with open('hot_query.txt', 'w') as f:
    for i in range(0,10000):
        f.write()