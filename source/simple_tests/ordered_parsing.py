#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pushdown

_parser = pushdown.Lark( r"""
start: ( terminal_name "\n" )+

terminal_name: TOKEN_NAME

TOKEN_NAME: /.+/
""", start='start', parser='lalr', lexer='contextual' )

tree = _parser.parse( "a\nb\nc\nd\ne\n" )

# print( tree )
print( tree.pretty() )
