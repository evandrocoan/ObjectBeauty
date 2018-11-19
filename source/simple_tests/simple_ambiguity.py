#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pushdown

_parser = pushdown.Lark( r"""
start: a b

a: "A" "B"

b: "AB"
""", start='start', parser='lalr', lexer='contextual' )


tree = _parser.parse( "AB\nBABAB" )

print( tree.pretty() )
