#
# This example demonstrates usage of the Indenter class.
#
# Since indentation is context-sensitive, a postlex stage is introduced to
# manufacture INDENT/DEDENT tokens.
#
# It is crucial for the indenter that the NL_type matches
# the spaces (and tabs) after the newline.
#

import os
from lark import Lark
from lark.indenter import Indenter

tree_grammar = r"""
    ?start: _NL* tree
    tree: NAME _NL [_INDENT tree+ _DEDENT]
    %import common.CNAME -> NAME
    %import common.WS_INLINE
    %declare _INDENT _DEDENT
    %ignore WS_INLINE
    _NL: /(\r?\n[\t ]*)+/
"""

class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 2

parser = Lark(tree_grammar, parser='lalr', postlex=TreeIndenter())

test_tree = """
a
    b
    c
        d
        e
    f
        g
"""

# To generate the lexer/parser
# python3 -m lark.tools.standalone ./grammars_grammar.lark > lexer.py
def test():
    tree = parser.parse(test_tree)
    print(tree.pretty())


if __name__ == '__main__':
    test()

