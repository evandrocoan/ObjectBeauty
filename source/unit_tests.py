import os
import sys
import debug_tools

import pushdown
import semantic_analyzer
import code_highlighter

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

def findCaller():
    return log.findCaller()

def getCallerName():
    return findCaller()[2]


class TestingGrammarUtilities(TestingUtilities):

    def _getParser(self, log_level):

        ## The relative path the the pushdown grammar parser file from the current file
        grammar_file_path = get_relative_path( "grammars_grammar.pushdown", __file__ )

        ## The parser used to build the Abstract Syntax Tree and parse the input text
        with open( grammar_file_path, "r", encoding='utf-8' ) as file:
            my_parser = pushdown.Lark( file.read(), start='language_syntax', parser='lalr', lexer='contextual', debug=log_level)
            return my_parser

    def _getError(self, example_grammar, return_tree=False, log_level=0):
        my_parser = self._getParser(log_level)
        tree = my_parser.parse(example_grammar)

        function_file = get_relative_path( "examples/%s.png" % getCallerName(), __file__ )
        # make_png( tree, get_relative_path( function_file, __file__ ) )

        # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
        # log( 1, "%s", getCallerName() )
        # log( 1, "%s", inspect.stack()[1][3] )

        if return_tree:
            new_tree = semantic_analyzer.TreeTransformer().transform( tree )

            # log( 1, 'tree: \n%s', tree.pretty() )
            # log( 1, 'tree: \n%s', new_tree.pretty() )
            return new_tree

        else:
            with self.assertRaises( semantic_analyzer.SemanticErrors ) as error:
                new_tree = semantic_analyzer.TreeTransformer().transform( tree )

            return error


class TestSemanticRules(TestingGrammarUtilities):

    def test_duplicatedContext(self):
        example_grammar = \
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
        error = self._getError(example_grammar)

        self.assertTextEqual(
        r"""
            + 1. Extra `contexts` rule defined in your grammar on [@-1,219:226='contexts'<__ANON_1>,10:13]
        """, error.exception )

    def test_duplicatedIncludes(self):
        example_grammar = \
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
        error = self._getError(example_grammar)

        self.assertTextEqual(
        r"""
            + 1. Duplicated include `duplicate` defined in your grammar on [@-1,385:393='duplicate'<__ANON_1>,17:13]
        """, error.exception )

    def test_missingIncludeDetection(self):
        example_grammar = \
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
        error = self._getError(example_grammar)

        self.assertTextEqual(
        r"""
            + 1. Missing include `missing_include` defined in your grammar on [@-1,215:229='missing_include'<TEXT_CHUNK_END_>,8:24]
        """, error.exception )

    def test_invalidRegexInput(self):
        example_grammar = \
        r"""
            name: Abstract Machine Language
            scope: source.sma
            contexts: {
              match: (true|false {
                scope: constant.language
              }
            }
        """
        error = self._getError(example_grammar)

        self.assertTextEqual(
        r"""
            + 1. Invalid regular expression `(true|false` on match statement: missing ), unterminated subpattern at position 0
        """, error.exception )

    def test_duplicatedGlobalNames(self):
        example_grammar = \
        r"""
            name: Abstract Machine Language
            name: Abstract Machine Language
            scope: source.sma
            scope: source.sma
            contexts: {
                match: (true|false) {
              }
            }
        """
        error = self._getError(example_grammar)

        self.assertTextEqual(
        r"""
            + 1. Duplicated target language name defined in your grammar on [@-1,63:87='Abstract Machine Language'<TEXT_CHUNK_END_>,3:19]
            + 2. Duplicated master scope name defined in your grammar on [@-1,138:147='source.sma'<TEXT_CHUNK_END_>,5:20]
        """, error.exception )

    def test_missingScopeGlobalName(self):
        example_grammar = \
        r"""
            name: Abstract Machine Language
            contexts: {
                match: (true|false) {
              }
            }
        """
        error = self._getError(example_grammar)

        self.assertTextEqual(
        r"""
            + 1. Missing master scope name in your grammar preamble.
        """, error.exception )

    def test_missingNameGlobal(self):
        example_grammar = \
        r"""
            scope: source.sma
            contexts: {
                match: (true|false) {
              }
            }
        """
        error = self._getError(example_grammar)

        self.assertTextEqual(
        r"""
            + 1. Missing target language name in your grammar preamble.
        """, error.exception )

    def test_unsusedInclude(self):
        example_grammar = \
        r"""
            scope: source.sma
            name: Abstract Machine Language
            contexts: {
                match: (true|false) {
              }
            }

            unused: {
                match: (true|false) {
              }
            }
        """
        error = self._getError(example_grammar)

        self.assertTextEqual(
        r"""
            +   Warnings:
            + 1. Unused include `unused` defined in your grammar on [@-1,180:185='unused'<__ANON_1>,9:13]
        """, error.exception )

    def test_unsusedConstantDeclaration(self):
        example_grammar = \
        r"""
            scope: source.sma
            name: Abstract Machine Language
            $constant: test
            contexts: {
                match: (true|false) {
              }
            }
        """
        error = self._getError(example_grammar)

        self.assertTextEqual(
        r"""
            +   Warnings:
            + 1. Unused constant `$constant:` defined in your grammar on [@-1,87:96='$constant:'<CONSTANT_NAME_>,4:13]
        """, error.exception )

    def test_constantUsage(self):
        example_grammar = \
        r"""
            scope: source.sma
            name: Abstract Machine Language
            $constant:  test
            contexts: {
                match: (true$constant:|false)$constant: {
              }
            }
        """
        tree = self._getError(example_grammar, True)

        self.assertTextEqual(
        r"""
            + language_syntax
            +   preamble_statements
            +     master_scope_name_statement  source.sma
            +     target_language_name_statement  Abstract Machine Language
            +      test
            +   language_construct_rules
            +     indentation_block
            +       statements_list
            +         match_statement  (true test|false) test
        """, tree.pretty(debug=0) )

    def test_isolatedConstantUsage(self):
        my_parser = pushdown.Lark(
        r"""
            free_input_string: ( constant_usage | TEXT_CHUNK )* ( TEXT_CHUNK_END_ | )
            TEXT_CHUNK: /(\\{|\\}|\\\$|[^\n{}\$])+(?=\$)/
            TEXT_CHUNK_END_: /(\\{|\\}|\\\$|[^\n{}\$])+(?!{)/
            constant_usage: CONSTANT_USAGE_
            CONSTANT_USAGE_: /\$[^\n\$\:]+\:(?!{)/
        """,
        start='free_input_string', parser='lalr', lexer='contextual')
        tree = my_parser.parse( "true$constant:|false" )

        self.assertTextEqual(
        r"""
            + free_input_string
            +   [@1,0:3='true'<TEXT_CHUNK>,1:1]
            +   constant_usage  [@2,4:13='$constant:'<CONSTANT_USAGE_>,1:5]
            +   [@3,14:19='|false'<TEXT_CHUNK_END_>,1:15]
        """, tree.pretty(debug=True) )

    def test_redifinedConst(self):
        example_grammar = \
        r"""
            scope: source.sma
            name: Abstract Machine Language
            $constant: test
            contexts: {
              $constant: test
                match: (true$constant:|false) {
              }
            }
        """
        error = self._getError(example_grammar)

        self.assertTextEqual(
        r"""
            + 1. Constant redefinition on [@-1,141:150='$constant:'<CONSTANT_NAME_>,6:15]
        """, error.exception )

    def test_recursiveConstantDefinition(self):
        example_grammar = \
        r"""
            scope: source.sma
            name: Abstract Machine Language
            $constant:  test$constant:
            contexts: {
                match: (true$constant:|false) {
              }
            }
        """
        error = self._getError(example_grammar)

        self.assertTextEqual(
        r"""
            +   Warnings:
            + 1. Recursive constant definition on [@-1,87:96='$constant:'<CONSTANT_NAME_>,4:13]
        """, error.exception )

    def test_usingConstOutOfScope(self):
        example_grammar = \
        r"""
            scope: source.sma
            name: Abstract Machine Language
            contexts: {
                match: (true$constant:|false) {
              }
              $constant: test
            }
        """
        error = self._getError(example_grammar)

        self.assertTextEqual(
        r"""
            + 1. Using constant `$constant:` out of scope on
            +    [@-1,127:136='$constant:'<CONSTANT_USAGE_>,5:29] from
            +    [@-1,177:186='$constant:'<CONSTANT_NAME_>,7:15]
        """, error.exception )

    def test_usingConstOutOfBlockDefinition(self):
        example_grammar = \
        r"""
            scope: source.sma
            name: Abstract Machine Language
            contexts: {
                $constant: test:
                match: (true $constant:|false) {
                  include: block
              }
            }

            block: {
                match: ($constant:) {
              }
            }
        """
        error = self._getError(example_grammar)

        self.assertTextEqual(
        r"""
            + 1. Using constant `$constant:` out of block on
            +    [@-1,290:299='$constant:'<CONSTANT_USAGE_>,12:25] from
            +    [@-1,115:124='$constant:'<CONSTANT_NAME_>,5:17]
        """, error.exception )


class TestBackEnd(TestingGrammarUtilities):

    def _getBackend(self, example_grammar, example_program, example_theme):
        function_file = get_relative_path( "examples/%s.html" % getCallerName(), __file__ )
        # log( 1, "function_file: %s", function_file )

        tree = self._getError(example_grammar, True)
        backend = code_highlighter.Backend(tree, example_program, example_theme)
        generated_html = backend.generated_html()

        with open( function_file, 'w', newline='\n', encoding='utf-8' ) as output_file:
            output_file.write( generated_html )
            output_file.write("\n")

        return generated_html

    def test_simpleMatchStamement(self):
        example_grammar = \
        r"""
            scope: source.sma
            name: Abstract Machine Language
            contexts: {
              match: (true|false) {
                scope: boolean.sma
              }
            }
        """

        example_program = \
        r"""true"""

        example_theme = \
        {
            "boolean" : "#FF0000",
        }

        generated_html = self._getBackend(example_grammar, example_program, example_theme)

        self.assertTextEqual(
        r"""
            + <!DOCTYPE html><html><head><title>Abstract Machine Language - source.sma</title></head>
            + <body style="white-space: pre; font-family: monospace;"><font color="#FF0000" grammar_scope="boolean.sma" theme_scope="boolean">true</font></body></html>
        """, generated_html )

    def test_unmatchedProgramCompletionAtEnd(self):
        example_grammar = \
        r"""
            scope: source.sma
            name: Abstract Machine Language
            contexts: {
              match: // {
                scope: comment.line.start.sma
              }
            }
        """

        example_program = \
        r"""
            // Example single line commentary
        """

        example_theme = \
        {
            "comment" : "#FF0000",
        }

        generated_html = self._getBackend(example_grammar, example_program, example_theme)

        self.assertTextEqual(
        r"""
            + <!DOCTYPE html><html><head><title>Abstract Machine Language - source.sma</title></head>
            + <body style="white-space: pre; font-family: monospace;"><font color="#FF0000" grammar_scope="comment.line.start.sma" theme_scope="comment">//</font><span grammar_scope="none" theme_scope="none"> Example single line commentary<br />        </span></body></html>
        """, generated_html )

    def test_unmatchedProgramCompletionAtMiddle(self):
        example_grammar = \
        r"""
            scope: source.sma
            name: Abstract Machine Language
            contexts: {
              match: // {
                scope: comment.line.start.sma
              }
              match: single {
                scope: comment.middle.start.sma
              }
            }
        """

        example_program = \
        r"""
            // Example single line commentary
        """

        example_theme = \
        {
            "comment" : "#FF0000",
        }

        generated_html = self._getBackend(example_grammar, example_program, example_theme)

        self.assertTextEqual(
        r"""
            + <!DOCTYPE html><html><head><title>Abstract Machine Language - source.sma</title></head>
            + <body style="white-space: pre; font-family: monospace;"><font color="#FF0000" grammar_scope="comment.line.start.sma" theme_scope="comment">//</font><span grammar_scope="none" theme_scope="none"> Example </span><font color="#FF0000" grammar_scope="comment.middle.start.sma" theme_scope="comment">single</font><span grammar_scope="none" theme_scope="none"> line commentary<br />        </span></body></html>
        """, generated_html )

    def test_simplePushPopStatement(self):
        example_grammar = \
        r"""
            scope: source.sma
            name: Abstract Machine Language
            contexts: {
              match: // {
                scope: comment.start.sma
                push: {
                  meta_scope: comment.line.sma
                  match: \n {
                    pop: true
                  }
                }
              }
            }
        """

        example_program = \
        r"""
            // Example single line commentary
        """

        example_theme = \
        {
            "comment" : "#FF0000",
            "comment.line" : "#00FF00",
        }

        generated_html = self._getBackend(example_grammar, example_program, example_theme)

        self.assertTextEqual(
        r"""
            + <!DOCTYPE html><html><head><title>Abstract Machine Language - source.sma</title></head>
            + <body style="white-space: pre; font-family: monospace;"><font color="#FF0000" grammar_scope="comment.start.sma" theme_scope="comment">//</font><font color="#00FF00" grammar_scope="comment.line.sma" theme_scope="comment.line"> Example single line commentary<br /></font><span grammar_scope="none" theme_scope="none">        </span></body></html>
        """, generated_html )

    def test_complexGrammarFile(self):
        example_grammar = \
        r"""
            scope: source.sma
            name: Abstract Machine Language
            contexts: {
              include: pawn_comment
              include: pawn_boolean
              include: pawn_preprocessor
              include: pawn_string
              include: pawn_function
            }
            pawn_boolean: {
              match: (true|false) {
                scope: boolean.sma
              }
            }
            pawn_comment: {
              match: /\*.*\*/ {
                scope: comment.block.documentation.sma
              }
            }
            pawn_preprocessor: {
              match: \s*#define {
                scope: function.definition.sma
                push: {
                  meta_scope: meta.preprocessor.sma
                  match: \n {
                    pop: true
                  }
                }
              }
            }
            pawn_string: {
              match: "(?=.*") {
                scope: punctuation.definition.string.begin.sma
                push: {
                  meta_scope: string.quoted.double.sma
                  match: "(?!.*") {
                    scope: punctuation.definition.string.end.sma
                    pop: true
                  }
                }
              }
            }
            pawn_function: {
              match: (\w+)\s*(\(.*\)) {
                scope: function.call.sma
              }
            }
        """

        example_program = debug_tools.utilities.wrap_text(
        r"""
            /* Commentary example */ true or false
            #define GLOBAL_CONSTANT
            var string = "My string definition"
            void function() {
            }
        """ )

        example_theme = \
        {
            "boolean" : "#FF0000",
            "comment" : "#00FF00",
            "function" : "#DDB700",
            "meta" : "#0000FF",
            "storage" : "#8000FF",
            "string" : "#808080",
            "punctuation" : "#FF0000",
        }

        generated_html = self._getBackend(example_grammar, example_program, example_theme)

        self.assertTextEqual(
        r"""
            + <!DOCTYPE html><html><head><title>Abstract Machine Language - source.sma</title></head>
            + <body style="white-space: pre; font-family: monospace;"><font color="#00FF00" grammar_scope="comment.block.documentation.sma" theme_scope="comment">/* Commentary example */</font><span grammar_scope="none" theme_scope="none"> </span><font color="#FF0000" grammar_scope="boolean.sma" theme_scope="boolean">true</font><span grammar_scope="none" theme_scope="none"> or </span><font color="#FF0000" grammar_scope="boolean.sma" theme_scope="boolean">false</font><font color="#DDB700" grammar_scope="function.definition.sma" theme_scope="function"><br />#define</font><font color="#0000FF" grammar_scope="meta.preprocessor.sma" theme_scope="meta"> GLOBAL_CONSTANT<br /></font><span grammar_scope="none" theme_scope="none">var string = </span><font color="#FF0000" grammar_scope="punctuation.definition.string.begin.sma" theme_scope="punctuation">"</font><font color="#808080" grammar_scope="string.quoted.double.sma" theme_scope="string">My string definition</font><font color="#FF0000" grammar_scope="punctuation.definition.string.end.sma" theme_scope="punctuation">"</font><span grammar_scope="none" theme_scope="none"><br />void </span><font color="#DDB700" grammar_scope="function.call.sma" theme_scope="function">function()</font><span grammar_scope="none" theme_scope="none"> {<br />}</span></body></html>
        """, generated_html )


if __name__ == "__main__":
    main()
