#!/bin/sh

. ./common.sh
rm -f /tmp/a.pcap

(cd $TREX_CORE; ./stl-sim -f $SCRIPTPATH/autotrex/$TREX_INPUT_FILE \
               -o /tmp/a.pcap > $SCRIPTPATH/stl-sim.log 2>&1)

tcpdump -r /tmp/a.pcap -nnn -c 10 -t
