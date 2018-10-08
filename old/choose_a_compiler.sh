#!/bin/sh


CURRENT_PATH=$(pwd)
COMMAND_TO_RUN="pwd; echo $CURRENT_PATH; cd $CURRENT_PATH; sh make_run.sh $@"

echo "choose_a_compiler.sh: $CURRENT_PATH"



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











