
import os
import lark
import semantic_analyzer

from lark import Lark
from lark.indenter import Indenter

def make_png(lark_tree, output_file):
    lark.tree.pydot__tree_to_png( lark_tree, output_file)

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
    meu_parser = Lark( file.read(), start='language_syntax', parser='lalr', lexer='contextual', transformer=semantic_analyzer.TreeTransformer )

simples_exemplo = """
name: Abstract Machine Language
scope: source.sma
contexts:
    match: (true|false)
        scope: constant.language
"""

"""
apt-cyg update
awk: cmd. line:4: fatal: cannot open file `/etc/setup/setup.rc' for reading (No such file or directory)
awk: fatal: cannot open file `/etc/setup/setup.rc' for reading (No such file or directory)
mkdir: cannot create directory ‘//x86’: Read-only file system
/usr/bin/apt-cyg: line 158: cd: //x86: No such file or directory
/x86/setup.bz2: Scheme missing.
Error updating setup.ini, reverting
"""

# To generate the lexer/parser
# python3 -m lark.tools.standalone /cygdrive/l/Arquivos/gramatica_compiladores.lark > lexer.py
def test():
    # tree = meu_parser.parse(simples_exemplo)
    # print(tree.pretty())
    # grammar_file_path = get_relative_path( "exemplos/programa_exemplo.beauty-grammar", __file__ )
    grammar_file_path = get_relative_path( "exemplos/duplicated_contexts.beauty-grammar", __file__ )

    with open( grammar_file_path, "r", encoding='utf-8' ) as file:
        tree = meu_parser.parse(file.read())
        # print(tree.pretty())
        make_png( tree, get_relative_path( "exemplos/duplicated_contexts.png", __file__ ) )

if __name__ == '__main__':
    test()

