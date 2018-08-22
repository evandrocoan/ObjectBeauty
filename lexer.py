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

def get_relative_path(relative_path, script_file):
    """
        Computes a relative path for a file on the same folder as this class file declaration.
        https://stackoverflow.com/questions/4381569/python-os-module-open-file-above-current-directory-with-relative-path
    """
    basepath = os.path.dirname( script_file )
    filepath = os.path.abspath( os.path.join( basepath, relative_path ) )
    return filepath

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

# parser = Lark(tree_grammar, parser='lalr', postlex=TreeIndenter())

## The relative path the the lark grammar parser file from the current file
grammar_file_path = get_relative_path( "gramatica_compiladores.lark", __file__ )

with open( grammar_file_path, "r", encoding='utf-8' ) as file:
    ## The parser used to build the Abstract Syntax Tree and parse the input text
    # meu_parser = Lark( file.read(), start='language_syntax', lexer='standard', parser='lalr', postlex=TreeIndenter() )
    meu_parser = Lark( file.read(), start='language_syntax', parser='lalr', postlex=TreeIndenter() )

test_tree = """
a
    b
    c
        d
        e
    f
        g
"""

simples_exemplo = """
name: Abstract Machine Language
scope: source.sma
contexts:
    match: (true|false)
        scope: constant.language
"""
"""
  main:
"""
# To generate the lexer/parser
# python3 -m lark.tools.standalone /cygdrive/l/Arquivos/gramatica_compiladores.lark > lexer.py
def test():
    # print(parser.parse(test_tree).pretty())
    # tree = meu_parser.parse(simples_exemplo)
    # print(tree.pretty())
    grammar_file_path = get_relative_path( "programa_exemplo_simples.beauty-grammar", __file__ )

    with open( grammar_file_path, "r", encoding='utf-8' ) as file:
        ## The parser used to build the Abstract Syntax Tree and parse the input text
        # meu_parser = Lark( file.read(), start='language_syntax', lexer='standard', parser='lalr', postlex=TreeIndenter() )
        tree = meu_parser.parse(file.read())
        print(tree.pretty())


if __name__ == '__main__':
    test()

