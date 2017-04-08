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
 * Scope Blocks
 *
 * A ScopeBlock object only contains the information for its own scope type. Through the program
 * execution there will be several scopes typings. Initially the type `ScopeBlock` will only
 * generate basic scope types as `c++_like_block_comment`.
 *
 * Later when the `FormattingRule` type start walking through the source code to perform the
 * formatting, there will be created the compound scopes types based on the basic scope types math
 * as `all_blocks - c++_like_block_comment`.
 *
 * The responsibility of the `ScopeBlock` objects are to hold the:
 *     1. The current scope type(s) as `all_blocks - c++_like_block_comment`
 *     2. Scope start(s)/end(s)
 *     3. A continuous iterator through the whole scope skipping wholes
 */
class ScopeBlock
{
public:
    ScopeBlock()
    {
        LOG( b1, "ScopeBlock::ScopeBlock(0)" );
    }

    ~ScopeBlock()
    {
        LOG( b1, "    ( ~ScopeBlock ) The object is being deleted." );
    }

private:
    std::string text_code;

};





