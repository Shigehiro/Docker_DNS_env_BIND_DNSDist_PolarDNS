#!/bin/sh

sleep 3

if [ -e /dnsdist.conf ]
then
  dnsdist -C /dnsdist.conf --disable-syslog --supervised
else
  dnsdist -C /etc/dnsdist/dnsdist.conf --disable-syslog --supervised
fi
