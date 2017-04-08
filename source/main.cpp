/*********************** Licensing *******************************************************
*
*   Copyright 2017 @ Evandro Coan
*
*   Program Main Page: https://github.com/evandrocoan/ObjectBeautifier
*
*  This program is free software; you can redistribute it and/or modify it
*  under the terms of the GNU General Public License as published by the
*  Free Software Foundation; either version 3 of the License, or ( at
*  your option ) any later version.
*
*  This program is distributed in the hope that it will be useful, but
*  WITHOUT ANY WARRANTY; without even the implied warranty of
*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
*  General Public License for more details.
*
*  You should have received a copy of the GNU General Public License
*  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*****************************************************************************************
*/

#include "headers/debugger.h"
#include "classes/SourceCode.cpp"
#include "yaml-cpp/yaml.h"

#include <iostream>
#include <sstream>
#include <cstdlib>
#include <exception>

#include <fstream>
#include <string>
#include <vector>

void term_func()
{
   std::cout << "\n\n\nterm_func was called by terminate.\n\n\n\n" << std::endl;
   exit( EXIT_FAILURE );
}

/**
 * Start the program execution and read the program argument list passed to it. This program
 * accept none or one command line argument.
 *
 * An example call to this program could be:
 * ./main.o solved.txt
 *
 * @param argumentsCount         one plus the argument counting passed to the program command line.
 * @param argumentsStringList    an argument list passed the program command line, where its first
 *                               string is current program execution path.
 *
 * @return the cstdlib::EXIT_SUCCESS on success, or EXIT_FAILURE on fail.
 */
int main( int argumentsCount, char* argumentsStringList[] )
{
    LOG( a2, "Starting the main program...\n" );
    LOG( a1, "argumentsCount: %d", argumentsCount );

    std::set_terminate( term_func );

    if( argumentsCount > 1 )
    {
        for( int argumentIndex = 0; argumentIndex < argumentsCount; argumentIndex++ )
        {
            LOG( a1, "argumentsStringList[%d]: %s", argumentIndex, argumentsStringList[ argumentIndex ] );
        }
    }

    std::cout << "YAML\n" << std::endl;

    // https://learnxinyminutes.com/docs/yaml/
    YAML::Node SyntaxFile = YAML::LoadFile("test.beauty-blocks");
    const YAML::Node& blockContexts = SyntaxFile["contexts"];

    try
    {
        for( auto it = blockContexts.begin(); it != blockContexts.end(); ++it )
        {
            const YAML::Node& sensor = *it;
            std::cout << "match: " << sensor["match"].as<std::string>() << "\n";
            std::cout << "scope: " << sensor["scope"].as<std::string>() << "\n\n";
        }
    }
    catch(...)
    {
        LOG( a1, "Exception!!!!" );
    }

    LOG( a1, "" );

    // Uniform initialization syntax to solve the Most vexing parse.
    SourceCode sourceCode{ "if(hi)" };

    // http://stackoverflow.com/questions/10595451/why-copy-constructor-is-called-here-instead-of-normal-constructor-and-overloaded
    SourceCode s2 = sourceCode;

    LOG( a1, "Exiting main(2)" );
    return EXIT_SUCCESS;
}






