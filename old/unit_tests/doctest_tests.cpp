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


#include "libraries/doctest/doctest/doctest.h"


unsigned int factorial( unsigned int number )
{
    return number <= 1 ? number : factorial(number-1)*number;
}

TEST_CASE("testing the factorial function")
{
    CHECK(factorial(1) == 1);
    CHECK(factorial(2) == 2);
    CHECK(factorial(3) == 6);
    CHECK(factorial(10) == 3628800);
}


