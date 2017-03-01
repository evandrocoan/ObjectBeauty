

if [[ $1 == "catch_tests" ]]
then
    make catch_tests
    ./main
elif [[ $1 == "veryclean" ]]
then
    make veryclean
else
    make clean
    make
    ./main argument1 argument2
fi


wait $!

