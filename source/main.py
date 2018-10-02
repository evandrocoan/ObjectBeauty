
import os
import lark
import semantic_analyzer

from lark import Lark
from lark.indenter import Indenter

from pprint import pformat
from debug_tools import getLogger

log = getLogger(__name__)


def make_png(lark_tree, output_file):
    lark.tree.pydot__tree_to_png( lark_tree, output_file, "TB")

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


# To generate the lexer/parser
# python3 -m lark.tools.standalone /cygdrive/l/Arquivos/gramatica_compiladores.lark > lexer.py
def test():
    # grammar_file_path = get_relative_path( "exemplos/programa_exemplo.beauty-grammar", __file__ )
    grammar_file_path = get_relative_path( "exemplos/duplicated_contexts.beauty-grammar", __file__ )

    with open( grammar_file_path, "r", encoding='utf-8' ) as file:
        tree = meu_parser.parse(file.read())
        # make_png( tree, get_relative_path( "exemplos/duplicated_contexts.png", __file__ ) )
        # log( 1, tree.pretty() )

        new_tree = semantic_analyzer.TreeTransformer().transform( tree )
        # make_png( tree, get_relative_path( "exemplos/duplicated_contexts.png", __file__ ) )
        log( 1, "\n%s", new_tree.pretty() )


if __name__ == '__main__':
    test()

