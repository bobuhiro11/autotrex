#!/bin/sh

# Get Trex core path.
TREX_CORE=${TREX_CORE:-/tmp/v3.02}

# Get current script path.
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# Search trex configuration.
TREX_CFG=${TREX_CFG:-$SCRIPTPATH/trex_cfg.yaml}

# Set PYTHONPATH.
export PYTHONPATH=$TREX_CORE/trex_control_plane/interactive/trex/examples/stl:$PYTHONPATH
export PYTHONPATH=$TREX_CORE/automation/trex_control_plane/interactive:$PYTHONPATH

# Get input file.
export TREX_INPUT_FILE=${1:-tcp_1pkt_rand.py}
