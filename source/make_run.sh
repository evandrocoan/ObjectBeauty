#!/bin/sh


# Import the helper functions.
. ./timer_calculator.sh


FIRST_COMMAND_ARGUMENT=$1

runMainProgram()
{
    printf "\n"

    if ./main
    then
        printf "Successfully ran \`./main\`.\n"
    else
        printf "Could not run \`./main\` properly!\n"
        exit 1
    fi
}


if [[ $FIRST_COMMAND_ARGUMENT == "main" ]]
then
    if make
    then
        runMainProgram
    fi

elif [[ $FIRST_COMMAND_ARGUMENT == "veryclean" ]]
then
    make $FIRST_COMMAND_ARGUMENT

    if make
    then
        runMainProgram
    fi

elif [[ $FIRST_COMMAND_ARGUMENT == "visual_studio" ]]
then
    cur_dir=$(pwd)

    mkdir -p libraries/yaml-cpp/bin_msvs
    cd libraries/yaml-cpp/bin_msvs

    cmake -G "Visual Studio 14 2015" ../
    vs.bat devenv YAML_CPP.sln /Build Release

    printf "\n"
    cd $cur_dir

    if make $FIRST_COMMAND_ARGUMENT
    then
        runMainProgram
    fi

else
    if make $FIRST_COMMAND_ARGUMENT
    then
        runMainProgram
    fi

fi


wait $!
showTheElapsedSeconds "$0"


