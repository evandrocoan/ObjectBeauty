#!/bin/sh

# Import the helper functions.
. ../scripts/timer_calculator.sh



# make clean
make

# pwd
# cp proposal/.cache/main.pdf ./proposal.pdf


wait $!
showTheElapsedSeconds "$0"


