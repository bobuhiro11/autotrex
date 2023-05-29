#!/bin/sh

. ./common.sh

pkill -f t-rex-64

(cd $TREX_CORE;
 nohup ./t-rex-64 -i --cfg $TREX_CFG > $SCRIPTPATH/t-rex-64.log 2>&1 &)

sleep 10
cat $TREX_CFG
cat $SCRIPTPATH/t-rex-64.log
echo "trex server started."
python3 -m autotrex.benchmark
