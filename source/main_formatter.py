#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

####################### Licensing #######################################################
#
#   Copyright 2019 @ Evandro Coan
#   Source Code Formatter Example
#
#  Redistributions of source code must retain the above
#  copyright notice, this list of conditions and the
#  following disclaimer.
#
#  Redistributions in binary form must reproduce the above
#  copyright notice, this list of conditions and the following
#  disclaimer in the documentation and/or other materials
#  provided with the distribution.
#
#  Neither the name Evandro Coan nor the names of any
#  contributors may be used to endorse or promote products
#  derived from this software without specific prior written
#  permission.
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or ( at
#  your option ) any later version.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################################
#

import os
import sys
import pushdown
import semantic_analyzer

from pushdown import Lark
from debug_tools import getLogger

log = getLogger(__name__)

def assert_path(module):
    if module not in sys.path:
        sys.path.append( module )

assert_path( os.path.realpath( __file__ ) )
from utilities import make_png
from debug_tools.utilities import get_relative_path

## The relative path the the pushdown grammar parser file from the current file
grammar_path = get_relative_path( "examples/duplicated_contexts.beauty-grammar", __file__ )
metagrammar_path = get_relative_path( "grammars_grammar.pushdown", __file__ )

## The parser used to build the Abstract Syntax Tree and parse the input text
with open( metagrammar_path, "r", encoding='utf-8' ) as file:
    my_parser = Lark( file.read(), start='language_syntax', parser='lalr', lexer='contextual')

with open( grammar_path, "r", encoding='utf-8' ) as file:
    syntax_tree = my_parser.parse(file.read())
    make_png( syntax_tree, get_relative_path( "examples/duplicated_contexts.png", __file__ ), debug=True )

    # print the Syntax Tree to the console
    log( "Syntax Tree\n%s", syntax_tree.pretty() )
    abstract_syntax_tree = semantic_analyzer.TreeTransformer().transform( syntax_tree )

    # make_png( syntax_tree, get_relative_path( "examples/duplicated_contexts.png", __file__ ) )
    log( "Abstract Syntax Tree\n%s", abstract_syntax_tree.pretty( debug=True ) )

    backend = code_formatter.Backend( code_formatter.SingleSpaceFormatter, tree, example_program, example_theme )
    generated_html = backend.generated_html()

    with open( function_file, 'w', newline='\n', encoding='utf-8' ) as output_file:
        output_file.write( generated_html )
        output_file.write("\n")
