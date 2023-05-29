#!/bin/sh

set -x

# Search trex configuration.
if [ -z "$TREX_CFG" ]; then
  SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
  TREX_CFG=$SCRIPTPATH/trex_cfg.yaml
fi
cat $TREX_CFG


# Run trex server.
(cd $TREX_CORE; ./t-rex-64 -i --cfg $TREX_CFG)
