


FIRST_COMMAND_ARGUMENT=$1

if [[ $FIRST_COMMAND_ARGUMENT == "main" ]]
then
    make clean
    make
    ./main argument1 argument2

elif [[ $FIRST_COMMAND_ARGUMENT == "veryclean" ]]
then
    make $FIRST_COMMAND_ARGUMENT
    make
    ./main

else
    make clean
    make $FIRST_COMMAND_ARGUMENT
    ./main
fi


wait $!

