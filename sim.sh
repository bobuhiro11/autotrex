#!/bin/sh

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $TREX_CORE
rm -f /tmp/a.pcap
./stl-sim -f $SCRIPTPATH/tcp_1pkt.py \
          -o /tmp/a.pcap
tcpdump -r /tmp/a.pcap -nnn -e
