#!/bin/sh

# Convert windows bars as \ to linux one /
NEXT_PATH=$(echo $1 | sed -r "s|\\\|\/|g")

CURRENT_PATH=$(pwd)
COMMAND_TO_RUN="pwd; echo $NEXT_PATH; cd $NEXT_PATH; $2 $CURRENT_PATH"

echo "choose_a_compiler.sh: $NEXT_PATH"



current_terminal="mintty"

if command -v $current_terminal >/dev/null 2>&1; then
    /bin/$current_terminal -w max -h always -e /bin/bash --login -i -c "$COMMAND_TO_RUN"
    exit 0
fi



current_terminal="xfce4-terminal"

if command -v $current_terminal >/dev/null 2>&1; then
    /usr/bin/$current_terminal --maximize --hold --command="$COMMAND_TO_RUN"
    exit 0
fi



# TODO
# "konsole" "gnome-terminal" "xterm"











