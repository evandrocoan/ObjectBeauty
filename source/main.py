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

## The relative path the the lark grammar parser file from the current file
grammar_file_path = get_relative_path( "gramatica_compiladores.lark", __file__ )

## The parser used to build the Abstract Syntax Tree and parse the input text
with open( grammar_file_path, "r", encoding='utf-8' ) as file:
    meu_parser = Lark( file.read(), start='language_syntax', parser='lalr', lexer='contextual')

simples_exemplo = """
name: Abstract Machine Language
scope: source.sma
contexts:
    match: (true|false)
        scope: constant.language
"""

# To generate the lexer/parser
# python3 -m lark.tools.standalone /cygdrive/l/Arquivos/gramatica_compiladores.lark > lexer.py
def test():
    # tree = meu_parser.parse(simples_exemplo)
    # print(tree.pretty())
    grammar_file_path = get_relative_path( "programa_exemplo.beauty-grammar", __file__ )

    with open( grammar_file_path, "r", encoding='utf-8' ) as file:
        tree = meu_parser.parse(file.read())
        print(tree.pretty())


if __name__ == '__main__':
    test()

