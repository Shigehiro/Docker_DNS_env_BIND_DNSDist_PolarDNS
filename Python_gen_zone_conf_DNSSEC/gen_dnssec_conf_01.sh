#!/bin/sh

python3 ./generate_sub.sub.example.com.py -s 0 -e 10 &
python3 ./generate_sub.sub.delay.com.py -s 0 -e 10 &
python3 ./generate_sub.sub.example.com.py -s 10 -e 20 &
python3 ./generate_sub.sub.delay.com.py -s 10 -e 20 &
python3 ./generate_sub.sub.example.com.py -s 20 -e 30 &
python3 ./generate_sub.sub.delay.com.py -s 20 -e 30 &
python3 ./generate_sub.sub.example.com.py -s 30 -e 40 &
python3 ./generate_sub.sub.delay.com.py -s 30 -e 40 &
python3 ./generate_sub.sub.example.com.py -s 40 -e 50 &
python3 ./generate_sub.sub.delay.com.py -s 40 -e 50 &
python3 ./generate_sub.sub.example.com.py -s 50 -e 60 &
python3 ./generate_sub.sub.delay.com.py -s 50 -e 60 &
python3 ./generate_sub.sub.example.com.py -s 60 -e 70 &
python3 ./generate_sub.sub.delay.com.py -s 60 -e 70 &
python3 ./generate_sub.sub.example.com.py -s 70 -e 80 &
python3 ./generate_sub.sub.delay.com.py -s 70 -e 80 &
python3 ./generate_sub.sub.example.com.py -s 80 -e 90 &
python3 ./generate_sub.sub.delay.com.py -s 80 -e 90 &
python3 ./generate_sub.sub.example.com.py -s 90 -e 100 &
python3 ./generate_sub.sub.delay.com.py -s 90 -e 100 &
