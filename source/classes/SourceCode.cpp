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


#include <string>
#include "headers/debugger.h"

#pragma once

class SourceCode
{
public:
    SourceCode()
    {
        LOG( b1, "SourceCode::SourceCode(0)" );
    }

    SourceCode( std::string text_code ) : text_code( text_code )
    {
        LOG( b1, "SourceCode::SourceCode(1) text_code: %s", text_code );
    }

private:
    std::string text_code;

};





