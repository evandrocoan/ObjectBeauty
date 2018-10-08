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


#include <string>
#include "headers/debugger.h"

#pragma once

/**
 * General Scoping Rules
 *
 * Instead of always to writing the rule for opening and defining a commentary scope rule on every
 * settings files, create it at only one file per language characteristic scoping rules as aliases
 * which can be used across all settings files. We will not create one scoping setting file per
 * language because it would be pointless as the several languages uses the exactly construct tool.
 *
 * For example, the C++ block comments constructs /* *\/ are the same on C, Java and Pawn. So it
 * would be created one file per scoping concept as block comments. On this file all the scoping
 * rules for all languages will be defined and used across the configurations files.
 *
 * The responsibility of the `ScopeRule` objects are to hold the:
 *     1. Scope block name,
 *     2. Its start/end regular expression
 */
class ScopeRule
{
public:
    ScopeRule()
    {
        LOG( b1, "ScopeRule::ScopeRule(0)" );
    }

    ~ScopeRule()
    {
        LOG( b1, "    ( ~ScopeRule ) The object is being deleted." );
    }

private:
    std::string text_code;

};





