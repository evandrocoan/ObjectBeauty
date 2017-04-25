#!/bin/sh

# Import the helper functions.
. $1/timer_calculator.sh



# make clean
make

pwd
cp proposal/.cache/main.pdf ./proposal.pdf


wait $!
showTheElapsedSeconds "$0"


