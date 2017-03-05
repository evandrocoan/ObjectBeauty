


FIRST_COMMAND_ARGUMENT=$1

if [[ $FIRST_COMMAND_ARGUMENT == "main" ]]
then
    make clean
    make

elif [[ $FIRST_COMMAND_ARGUMENT == "veryclean" ]]
then
    make $FIRST_COMMAND_ARGUMENT
    make

else
    make clean
    make $FIRST_COMMAND_ARGUMENT
fi


wait $!

