

if [[ $1 == "catch_tests" ]]
then
    make catch_tests
    ./main
else
    make clean
    make
    ./main argument1 argument2
fi


wait $!

