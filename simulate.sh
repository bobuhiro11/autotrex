#!/bin/sh

. ./common.sh
rm -f /tmp/a.pcap

(cd $TREX_CORE; ./stl-sim -f $SCRIPTPATH/autotrex/$TREX_INPUT_FILE \
               -o /tmp/a.pcap)

tcpdump -r /tmp/a.pcap -nnn
