#!/bin/sh

. ./common.sh
rm -f /tmp/a.pcap

(cd $TREX_CORE; ./stl-sim -f $SCRIPTPATH/autotrex/tcp_1pkt.py \
               -o /tmp/a.pcap)

tcpdump -r /tmp/a.pcap -nnn -e
