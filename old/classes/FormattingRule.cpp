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
 * Formatting Performed Abstracted of Language
 *
 * The languages still existing, however the formatting will not be based on languages
 * but in the formatting based in visual formatting concepts.
 * There will not be a setting to add spaces in paren for java, c++, etc. There will be a
 * setting to add spaces in paren for specific regex and/or inclusion and exclusion laws
 * formed on that particular setting file, together within its Unit Tests.
 *
 * Basically a setting file it will be very big and complex and only will treat a specific
 * kind of visual formatting concept. Therefore to simply allow how to choose and setup a
 * visual style for your own taste or needs, not all settings will be loaded to be processed
 * and applied to parse the source code. Moreover not loading any settings file will imply
 * on a zero-configuration, i.e., nothing will be changed on the source code after the parsing.
 *
 * Each formatting rule file contains always the same blocks of data. Therefore a default
 * loader can be used for all settings to get their settings data from the disk. Also, each
 * setting will be loaded by its own thread, and not the opposite, first I read the setting
 * then I create the thread. Doing so increase the parallelism reality. Each rule setting
 * file will be equipped within the following data:
 *
 * The responsibility of the `FormattingRule` objects are to hold the:
 *     1. Rule Name
 *     2. Languages Inclusion
 *     3. Inclusion Block
 *     4. Exclusion Blocks
 */
class FormattingRule
{
public:
    FormattingRule()
    {
        LOG( b1, "FormattingRule::FormattingRule(0)" );
    }

    ~FormattingRule()
    {
        LOG( b1, "    ( ~FormattingRule ) The object is being deleted." );
    }

private:
    std::string text_code;

};





