import os
import sys
import lark
import semantic_analyzer

import unittest
import profile
import cProfile

from debug_tools import getLogger

log = getLogger( 127, os.path.basename( os.path.dirname( os.path.abspath ( __file__ ) ) ) )
log( 1, "Importing " + __name__ )

def assert_path(module):
    if module not in sys.path:
        sys.path.append( module )

assert_path( os.path.realpath( __file__ ) )

from testing_utilities import TestingUtilities
from testing_utilities import make_png
from testing_utilities import get_relative_path

def main():
    # https://stackoverflow.com/questions/6813837/stop-testsuite-if-a-testcase-find-an-error
    unittest.main(failfast=True)

class TestSemanticRules(TestingUtilities):

    def _getParser(self):

        ## The relative path the the lark grammar parser file from the current file
        grammar_file_path = get_relative_path( "gramatica_compiladores.lark", __file__ )

        ## The parser used to build the Abstract Syntax Tree and parse the input text
        with open( grammar_file_path, "r", encoding='utf-8' ) as file:
            my_parser = lark.Lark( file.read(), start='language_syntax', parser='lalr', lexer='contextual')
            return my_parser

    def test_duplicatedContext(self):
        example_program = \
        r"""
            name: Abstract Machine Language
            scope: source.sma
            contexts: {
              match: (true|false) {
                scope: constant.language
              }
            }

            contexts: {
              match: (true|false) {
                scope: constant.language
              }
            }
        """
        my_parser = self._getParser()
        tree = my_parser.parse(example_program)

        # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
        function_name = "exemplos/%s.png" % sys._getframe().f_code.co_name
        make_png( tree, get_relative_path( function_name, __file__ ) )
        # log( 1, function_name )
        # log( 1, tree.pretty() )

        with self.assertRaises( semantic_analyzer.SemanticErrors ) as error:
            new_tree = semantic_analyzer.TreeTransformer().transform( tree )

        self.assertTextEqual(
        r"""
            + 1. Extra `contexts` rule defined in your grammar on: [@-1,219:226='contexts'<__ANON_0>,10:13]
        """, error.exception )

    def test_duplicatedIncludes(self):
        example_program = \
        r"""
            name: Abstract Machine Language
            scope: source.sma
            contexts: {
              match: (true|false) {
                scope: constant.language
              }
            }

            duplicate: {
              match: (true|false) {
                scope: constant.language
              }
            }

            duplicate: {
              match: (true|false) {
                scope: constant.language
              }
            }
        """
        my_parser = self._getParser()
        tree = my_parser.parse(example_program)

        function_name = "exemplos/%s.png" % sys._getframe().f_code.co_name
        make_png( tree, get_relative_path( function_name, __file__ ) )
        # log( 1, function_name )
        # log( 1, tree.pretty() )

        with self.assertRaises( semantic_analyzer.SemanticErrors ) as error:
            new_tree = semantic_analyzer.TreeTransformer().transform( tree )

        self.assertTextEqual(
        r"""
            + 1. Duplicated include `duplicate` defined in your grammar on: [@-1,352:360='duplicate'<__ANON_0>,16:13]
        """, error.exception )

    def test_missingIncludeDetection(self):
        example_program = \
        r"""
            name: Abstract Machine Language
            scope: source.sma
            contexts: {
              match: (true|false) {
                scope: constant.language
              }
              include: missing_include
            }
        """
        my_parser = self._getParser()
        tree = my_parser.parse(example_program)

        function_name = "exemplos/%s.png" % sys._getframe().f_code.co_name
        make_png( tree, get_relative_path( function_name, __file__ ) )
        # log( 1, function_name )
        # log( 1, tree.pretty() )

        with self.assertRaises( semantic_analyzer.SemanticErrors ) as error:
            new_tree = semantic_analyzer.TreeTransformer().transform( tree )

        self.assertTextEqual(
        r"""
            + 1. Missing include ` missing_include` defined in your grammar on: [@-1,214:229=' missing_include'<__ANON_2>,8:23]
        """, error.exception )

    def test_validRegexInput(self):
        example_program = \
        r"""
            name: Abstract Machine Language
            scope: source.sma
            contexts: {
              match: (true|false {
                scope: constant.language
              }
            }
        """
        my_parser = self._getParser()
        tree = my_parser.parse(example_program)

        function_name = "exemplos/%s.png" % sys._getframe().f_code.co_name
        make_png( tree, get_relative_path( function_name, __file__ ) )
        # log( 1, function_name )
        # log( 1, tree.pretty() )

        with self.assertRaises( semantic_analyzer.SemanticErrors ) as error:
            new_tree = semantic_analyzer.TreeTransformer().transform( tree )

        self.assertTextEqual(
        r"""
            + 1. Invalid regular expression ` (true|false ` on match statement:
            +    missing ), unterminated subpattern at position 1
        """, error.exception )


if __name__ == "__main__":
    main()
