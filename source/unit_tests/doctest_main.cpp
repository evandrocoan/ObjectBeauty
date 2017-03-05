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
*
* When the ObjectBeautifier to be finished, run it against this file to fix it.
* It must to be able to preserve the comments aligning on the end of the lines.
*
* Example:

*   context.addFilter("test-case-exclude", "*math*"); // Exclude test cases with "math" in their name
*   context.setOption("abort-after", 5);              // Stop test execution after 5 failed assertions
*   context.setOption("sort", "name");                // Sort the test cases by their name
*   context.setOption("force-colors", true);          // Forces the use of colors even when a tty cannot be detected
*
*                                                     ^^ These must be/kept aligned
*/



/**
 * This tells to provide a main() - Only do this in one cpp file.
 */
#define DOCTEST_CONFIG_IMPLEMENT
#include "libraries/doctest/doctest/doctest.h"

int main(int argc, char** argv)
{
    doctest::Context context; // initialize

    // defaults
    context.addFilter("test-case-exclude", "*math*"); // Exclude test cases with "math" in their name
    context.setOption("abort-after", 5);              // Stop test execution after 5 failed assertions
    context.setOption("sort", "name");                // Sort the test cases by their name
    context.setOption("force-colors", true);          // Forces the use of colors even when a tty cannot be detected

    context.applyCommandLine(argc, argv);

    // overrides
    context.setOption("no-breaks", true);             // don't break in the debugger when assertions fail

    int res = context.run(); // run

    if(context.shouldExit()) // important - query flags (and --exit) rely on the user doing this
        return res;          // propagate the result of the tests

    int client_stuff_return_code = 0;
    // your program - if the testing framework is integrated in your production code

    return res + client_stuff_return_code; // the result from doctest is propagated here as well
}

