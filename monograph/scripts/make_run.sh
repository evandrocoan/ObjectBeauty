#!/bin/sh

# Reliable way for a bash script to get the full path to itself?
# http://stackoverflow.com/questions/4774054/reliable-way-for-a-bash-script-to-get-the-full-path-to-itself
pushd `dirname $0` > /dev/null
SCRIPT_FOLDER_PATH=`pwd`
popd > /dev/null

# Import the helper functions.
. $SCRIPT_FOLDER_PATH/timer_calculator.sh


cd $1

# make clean
$2


wait $!
showTheElapsedSeconds "$0"


