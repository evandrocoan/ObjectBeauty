import os
import sys
import lark
import semantic_analyzer

import inspect
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

from utilities import make_png
from debug_tools.utilities import get_relative_path
from debug_tools.testing_utilities import TestingUtilities

def main():
    # https://stackoverflow.com/questions/6813837/stop-testsuite-if-a-testcase-find-an-error
    unittest.main(failfast=True)

class TestSemanticRules(TestingUtilities):

    def _getParser(self):

        ## The relative path the the lark grammar parser file from the current file
        grammar_file_path = get_relative_path( "grammars_grammar.lark", __file__ )

        ## The parser used to build the Abstract Syntax Tree and parse the input text
        with open( grammar_file_path, "r", encoding='utf-8' ) as file:
            my_parser = lark.Lark( file.read(), start='language_syntax', parser='lalr', lexer='contextual')
            return my_parser

    def _getError(self, example_program):
        my_parser = self._getParser()
        tree = my_parser.parse(example_program)

        def findCaller():
            return log.findCaller()

        def getCallerName():
            return findCaller()[2]

        # function_name = "exemplos/%s.png" % getCallerName()
        # make_png( tree, get_relative_path( function_name, __file__ ) )

        # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
        # log( 1, "%s", getCallerName() )
        # log( 1, "%s", inspect.stack()[1][3] )

        with self.assertRaises( semantic_analyzer.SemanticErrors ) as error:
            new_tree = semantic_analyzer.TreeTransformer().transform( tree )

        return error

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
        error = self._getError(example_program)

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
              include: duplicate
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
        error = self._getError(example_program)

        self.assertTextEqual(
        r"""
            + 1. Duplicated include `duplicate` defined in your grammar on: [@-1,385:393='duplicate'<__ANON_0>,17:13]
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
        error = self._getError(example_program)

        self.assertTextEqual(
        r"""
            + 1. Missing include `missing_include` defined in your grammar on: [@-1,215:229='missing_include'<__ANON_2>,8:24]
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
        error = self._getError(example_program)

        self.assertTextEqual(
        r"""
            + 1. Invalid regular expression `(true|false ` on match statement:
            +    missing ), unterminated subpattern at position 0
        """, error.exception )

    def test_duplicatedGlobalNames(self):
        example_program = \
        r"""
            name: Abstract Machine Language
            name: Abstract Machine Language
            scope: source.sma
            scope: source.sma
            contexts: {
              meta_scope: meta.block.pawn
              match: (true|false) {
              }
            }
        """
        error = self._getError(example_program)

        self.assertTextEqual(
        r"""
            + 1. Duplicated target language name defined in your grammar on: [@-1,62:87=' Abstract Machine Language'<__ANON_2>,3:18]
            + 2. Duplicated master scope name defined in your grammar on: [@-1,137:147=' source.sma'<__ANON_2>,5:19]
        """, error.exception )

    def test_duplicatedGlobalNames(self):
        example_program = \
        r"""
            name: Abstract Machine Language
            name: Abstract Machine Language
            scope: source.sma
            scope: source.sma
            contexts: {
              meta_scope: meta.block.pawn
              match: (true|false) {
              }
            }
        """
        error = self._getError(example_program)

        self.assertTextEqual(
        r"""
            + 1. Duplicated target language name defined in your grammar on: [@-1,63:87='Abstract Machine Language'<__ANON_2>,3:19]
            + 2. Duplicated master scope name defined in your grammar on: [@-1,138:147='source.sma'<__ANON_2>,5:20]
        """, error.exception )

    def test_missingScopeGlobalName(self):
        example_program = \
        r"""
            name: Abstract Machine Language
            contexts: {
              meta_scope: meta.block.pawn
              match: (true|false) {
              }
            }
        """
        error = self._getError(example_program)

        self.assertTextEqual(
        r"""
            + 1. Missing master scope name in your grammar preamble.
        """, error.exception )

    def test_missingNameGlobal(self):
        example_program = \
        r"""
            scope: source.sma
            contexts: {
              meta_scope: meta.block.pawn
              match: (true|false) {
              }
            }
        """
        error = self._getError(example_program)

        self.assertTextEqual(
        r"""
            + 1. Missing target language name in your grammar preamble.
        """, error.exception )

    def test_unsusedInclude(self):
        example_program = \
        r"""
            scope: source.sma
            name: Abstract Machine Language
            contexts: {
              meta_scope: meta.block.pawn
              match: (true|false) {
              }
            }

            unused: {
              match: (true|false) {
              }
            }
        """
        error = self._getError(example_program)

        self.assertTextEqual(
        r"""
            +   Warnings:
            + 1. Unused include `unused` defined in your grammar on: [@-1,220:225='unused'<__ANON_0>,10:13]
        """, error.exception )


if __name__ == "__main__":
    main()
