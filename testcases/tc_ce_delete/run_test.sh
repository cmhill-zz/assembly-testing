#!/bin/bash

python ../../src/ceStatistic.py ./output.sam ./ceValues
python ../../src/ceOracle.py ./ceValues ./oracle.txt

exit 0