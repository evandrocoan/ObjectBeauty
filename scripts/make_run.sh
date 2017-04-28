#!/bin/sh

# Import the helper functions.
. ./timer_calculator.sh


cd $1

# make clean
$2


wait $!
showTheElapsedSeconds "$0"


