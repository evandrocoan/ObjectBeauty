#! /usr/bin/env python
# -*- coding: utf-8 -*-

import lark

_parser = lark.Lark( r"""
start: terminal_name

terminal_name: TOKEN_NAME

TOKEN_NAME: /ab/
""", start='start', parser='lalr', lexer='contextual' )

tree = _parser.parse( "ab" )

print( tree )
print( tree.pretty() )
