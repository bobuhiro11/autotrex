#!/bin/sh

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ip link add dut-p0 type veth peer name dut-p1
ip link set up dut-p0
ip link set up dut-p1

cd $TREX_CORE
./t-rex-64 -i --cfg $SCRIPTPATH/trex_cfg.yaml
