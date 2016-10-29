/*********************** Licensing *******************************************************
*
*   Copyright 2016 @ Evandro Coan
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
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <cstdlib>



/**
 * Start the program execution and read the program argument list passed to it. This program
 * accept none or one command line argument.
 *
 * An example call to this program could be:
 * cat sudoku_unsolved.txt | ./main.o sudoku_solved.txt
 *
 * @param argumentsCount         one plus the argument counting passed to the program command line.
 * @param argumentsStringList    an argument list passed the program command line, where its first
 *                               string is current program execution path.
 *
 * @return the cstdlib::EXIT_SUCCESS on success, or EXIT_FAILURE on fail.
 */
int main( int argumentsCount, char* argumentsStringList[] )
{
    FPRINTLN( 1, "Starting the main program..." );

    if( argumentsCount > 1 )
    {
        FPRINTLN( 1, "argumentsCount: %d, argumentsStringList[1]: %s", argumentsCount, argumentsStringList[ 1 ] );
    }
    
    return EXIT_SUCCESS;
}



