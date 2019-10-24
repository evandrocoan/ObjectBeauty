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

import code_formatter
import semantic_analyzer

from pushdown import Lark
from debug_tools import getLogger
from debug_tools.testing_utilities import wrap_text

program_name = "main_highlighter"
log = getLogger(__name__)

def assert_path(module):
    if module not in sys.path:
        sys.path.append( module )

assert_path( os.path.realpath( __file__ ) )
from utilities import make_png
from debug_tools.utilities import get_relative_path

## The relative path the the pushdown grammar parser file from the current file
metagrammar_path = get_relative_path( "grammars_grammar.pushdown", __file__ )

## The parser used to build the syntax tree and parse the input text
with open( metagrammar_path, "r", encoding='utf-8' ) as file:
    my_parser = Lark( file.read(), start='language_syntax', parser='lalr', lexer='contextual')

example_grammar = wrap_text(
r"""
    scope: source.sma
    name: Abstract Machine Language
    contexts: {
        match: if\( {
            scope: if.statement.definition
            push: {
                meta_scope: if.statement.body
                match: \) {
                    scope: if.statement.definition
                    pop: true
                }
            }
        }
    }
""" )

syntax_tree = my_parser.parse( example_grammar )
make_png( syntax_tree, get_relative_path( "%s_syntax_tree.png" % program_name, __file__ ), debug=0, dpi=300 )

log.clean( "Syntax Tree\n%s", syntax_tree.pretty( debug=1 ) )
abstract_syntax_tree = semantic_analyzer.TreeTransformer().transform( syntax_tree )

log.clean( "Abstract Syntax Tree\n%s", abstract_syntax_tree.pretty( debug=1 ) )
make_png( abstract_syntax_tree, get_relative_path( "%s_abstract_syntax_tree.png" % program_name, __file__ ), debug=0, dpi=300 )

example_program = wrap_text(
r"""
if(something) bar
""" )

example_settings = {
    "if.statement.body" : 2,
}

backend = code_formatter.Backend( code_formatter.SingleSpaceFormatter, abstract_syntax_tree, example_program, example_settings )
generated_html = backend.generated_html()

with open( "%s.html" % program_name, 'w', newline='\n', encoding='utf-8' ) as output_file:
    output_file.write( generated_html )
    output_file.write("\n")
