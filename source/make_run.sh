

if [[ $1 == "catch_tests" ]]
then
    make catch_tests
    ./main

elif [[ $1 == "doctest_tests" ]]
then
    make doctest_tests
    ./main

elif [[ $1 == "veryclean" ]]
then
    make veryclean
    make
    ./main argument1 argument2

else
    make clean
    make
    ./main argument1 argument2

fi


wait $!

