
import os
import sys
import pushdown
import semantic_analyzer

from pushdown import Lark
from pushdown.indenter import Indenter

from pprint import pformat
from debug_tools import getLogger

log = getLogger(__name__)

def assert_path(module):
    if module not in sys.path:
        sys.path.append( module )

assert_path( os.path.realpath( __file__ ) )
from utilities import make_png
from debug_tools.utilities import get_relative_path

## The relative path the the pushdown grammar parser file from the current file
grammar_file_path = get_relative_path( "grammars_grammar.pushdown", __file__ )

## The parser used to build the Abstract Syntax Tree and parse the input text
with open( grammar_file_path, "r", encoding='utf-8' ) as file:
    meu_parser = Lark( file.read(), start='language_syntax', parser='lalr', lexer='contextual')

# To generate the lexer/parser
# python3 -m pushdown.tools.standalone ./grammars_grammar.pushdown > lexer.py
def test():
    # grammar_file_path = get_relative_path( "examples/programa_exemplo.beauty-grammar", __file__ )
    grammar_file_path = get_relative_path( "examples/duplicated_contexts.beauty-grammar", __file__ )

    with open( grammar_file_path, "r", encoding='utf-8' ) as file:
        tree = meu_parser.parse(file.read())
        make_png( tree, get_relative_path( "examples/duplicated_contexts.png", __file__ ), debug=True )
        # log( 1, tree.pretty() )

        new_tree = semantic_analyzer.TreeTransformer().transform( tree )
        # make_png( tree, get_relative_path( "examples/duplicated_contexts.png", __file__ ) )
        log( 1, "\n%s", new_tree.pretty(debug=True) )


if __name__ == '__main__':
    test()

