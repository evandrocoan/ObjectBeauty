#!/bin/sh

# Import the helper functions.
. $1/timer_calculator.sh



# make clean
make

cp cache/main.pdf .


wait $!
showTheElapsedSeconds "$0"


