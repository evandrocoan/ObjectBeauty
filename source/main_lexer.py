

import os
import lexer
from lexer import Indenter

def get_relative_path(relative_path, script_file):
    """
        Computes a relative path for a file on the same folder as this class file declaration.
        https://stackoverflow.com/questions/4381569/python-os-module-open-file-above-current-directory-with-relative-path
    """
    basepath = os.path.dirname( script_file )
    filepath = os.path.abspath( os.path.join( basepath, relative_path ) )
    return filepath

class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 2


# To generate the lexer/parser
# python3 -m lark.tools.standalone /cygdrive/l/Arquivos/gramatica_compiladores.lark > lexer.py
def test():
    grammar_file_path = get_relative_path( "programa_exemplo.beauty-grammar", __file__ )
    parser = lexer.Lark_StandAlone( postlex=TreeIndenter() )

    with open( grammar_file_path, "r", encoding='utf-8' ) as file:
        ## The parser used to build the Abstract Syntax Tree and parse the input text
        tree = parser.parse(file.read())
        print(tree.pretty())


if __name__ == '__main__':
    test()

