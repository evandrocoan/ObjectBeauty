#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

####################### Licensing #######################################################
#
#   Copyright 2019 @ Evandro Coan
#   Source Code Formatter
#
#  Redistributions of source code must retain the above
#  copyright notice, this list of conditions and the
#  following disclaimer.
#
#  Redistributions in binary form must reproduce the above
#  copyright notice, this list of conditions and the following
#  disclaimer in the documentation and/or other materials
#  provided with the distribution.
#
#  Neither the name Evandro Coan nor the names of any
#  contributors may be used to endorse or promote products
#  derived from this software without specific prior written
#  permission.
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or ( at
#  your option ) any later version.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################################
#

import re
import pprint
import pushdown
import dominate
import debug_tools

from pushdown import Tree
from collections import OrderedDict

from debug_tools import getLogger
log = getLogger(1, __name__, time=0, tick=0, msecs=0)

def escape_html(input_text):
    return dominate.util.escape( input_text, quote=False ).replace("\n", "<br />" )

def get_div_doc(original_program):
    return '<span grammar_scope="none" setting_scope="none">%s</span>' % escape_html( original_program )

def get_font_doc(original_program, formatted_text, setting, grammar_scope, setting_scope):
    return '<span setting="%s" grammar_scope="%s" setting_scope="%s" original_program="%s">%s</span>' % (
            setting, grammar_scope, setting_scope, original_program, escape_html( formatted_text )
        )

def get_html_header(title):
    return debug_tools.utilities.wrap_text(
        r"""
            <!DOCTYPE html><html><head><title>%s</title></head>
            <body style="white-space: pre; font-family: monospace;">
        """ % ( title )
    )

def get_html_footer():
    return debug_tools.utilities.wrap_text(
        r"""
            </body></html>
        """
    )


class AbstractFormatter(object):
    """
        Represents a program as chunks of data as (text_chunk_start_position,
        text_chunk).
    """

    def __init__(self, program, settings):
        super().__init__()
        self.initial_size = len( program )
        self.program = program

        ## No need to sort the settings other than always having the some logs output
        self.settings = OrderedDict( sorted( settings.items(), key=lambda item: item ) )

        self.new_program = []
        self.cached_new_program = []
        log( 4, "program %s: `%s`", len( str( self.program ) ), self.program )

    def __str__(self):
        """
            Returns the current version of the program,
            after being cut by add_match().
        """
        return self.program

    __repr__ = __str__

    def get_new_program(self):
        """
            Sorts the list of (text_chunk_start_position, text_chunk) accordingly to
            `text_chunk_start_position` and return the new program as full string.
        """
        if self.cached_new_program: return self.cached_new_program

        fixed_program = sorted( self.new_program, key=lambda item: item[0] )
        fixed_program_len = len(fixed_program)
        assert len( self.program ) == self.initial_size, "Expected %s got %s" % ( self.initial_size, len(self.program) )

        # Copy the unmatched chunks of text into the final program on self.new_program
        for index in range( 0, fixed_program_len ):

            if index < fixed_program_len - 1:
                current_chunk = fixed_program[index]
                next_chunk = fixed_program[index+1]

                if current_chunk[1] < next_chunk[0]:
                    doc = get_div_doc( self.program[current_chunk[1]:next_chunk[0]] )
                    self.new_program.append( ( current_chunk[1], next_chunk[0], doc ) )

            else:
                current_chunk = fixed_program[index]

                if current_chunk[1] < len( self.program ):
                    doc = get_div_doc( self.program[current_chunk[1]:] )
                    self.new_program.append( ( current_chunk[1], len( self.program ), doc ) )

        # At the end of the process, we must to preserve the program size on self.program
        # for the correct merge with the text chunks processed
        assert len( self.program ) == self.initial_size, "Expected %s got %s" % ( self.initial_size, len(self.program) )
        fixed_program = sorted( self.new_program, key=lambda item: item[0] )
        fixed_program_len = len(fixed_program)

        log( 4, "fixed_program:\n%s", pprint.pformat( [( item[0], item[1], str(item[2]) )for item in fixed_program], indent=2, width=200 ) )
        log( 4, "cached_new_program: %s", self.cached_new_program )

        self.cached_new_program = [ item[2] for item in fixed_program ]
        return self.cached_new_program

    def get_theme(self, scope_name):

        def select():

            for setting_scopes, setting_value in self.settings.items():
                setting_scopes = setting_scopes.split( '.' )

                for index in range( 1, len(setting_scopes) + 1 ):
                    setting_scope = ".".join( [ setting_scopes[inner_index] for inner_index in range( 0, index ) ] )
                    log( 8, "setting_value: %s, comparing `%s` with `%s`", setting_value, scope_name, setting_scope )

                    if setting_scope == scope_name:
                        log( 8, "Selecting %s with %s", setting_scope, setting_value )
                        return setting_value, setting_scope

            return "", ""

        matched_setting, setting_scope = select()

        log( 8, "matched_setting: '%s' (on %s)", matched_setting, setting_scope )
        return matched_setting, setting_scope

    def add_match(self, scope_name, last_match_stack, match):
        log( 4, "add_match: %s", match )
        last_match_stack[-1].append(match)
        match_start = match.start(0)
        match_end = match.end(0)
        match_start, match_end = match_start, match_end

        self.program = self.program[:match_start] + "§" * ( match_end - match_start ) + self.program[match_end:]
        assert len( self.program ) == self.initial_size, "Expected %s got %s" % ( self.initial_size, len(self.program) )

        self._generate_chunk_html( scope_name, match[0], match_start, match_end )

    def add_meta_scope(self, scope_name, last_matches, match, ignore_last_match=False):
        """ ignore_last_match is set when the last_match value was already scoped,
            and as we only support scoping text one time, we have to ignore the last_match """
        log( 4, "add_meta_scope: %s", match )
        last_match = last_matches.pop() if last_matches else None
        match_end = match.end(0)

        if last_match:
            log( 4, "match.start: %s, match.end: %s", match.start(0), match.end(0) )
            log( 4, "last_match.start: %s, last_match.end: %s", last_match.start(0), last_match.end(0) )

            # match.start: 134, match.end: 135
            # last_match.start: 113, last_match.end: 114
            if ignore_last_match and match.start(0) > last_match.start(0):
                match_end = match.start(0)

            match_start = last_match.end(0)
            match_start, match_end = match_start, match_end

            self._generate_chunk_html( scope_name, self.program[match_start:match_end], match_start, match_end )
            self.program = self.program[:match_start] + "§" * ( match_end - match_start ) + self.program[match_end:]

        else:
            match_start = match.start(0)
            match_start, match_end = match_start, match_end

            self._generate_chunk_html( scope_name, self.program[match_start:match_end], match_start, match_end )
            self.program = self.program[:match_start] + "§" * ( match_end - match_start ) + self.program[match_end:]

        assert len( self.program ) == self.initial_size, "Expected %s got %s" % ( self.initial_size, len(self.program) )

    def _generate_chunk_html(self, grammar_scope, matched_text, match_start, match_end):
        matched_setting, setting_scope = self.get_theme(grammar_scope)

        if setting_scope:
            formatted_text = self.format_text( matched_text, matched_setting )
            html_fragment = get_font_doc( matched_text, formatted_text, matched_setting, grammar_scope, setting_scope )

        else:
            html_fragment = get_font_doc( matched_text, matched_text, "unformatted", grammar_scope, setting_scope )

        self.new_program.append( ( match_start, match_end, html_fragment ) )
        log( 4, "formatted_text: %s", html_fragment )
        log( 4, "program %s: `%s`", len( str( self.program ) ), self.program )

    def format_text(matched_text, matched_setting):
        return matched_text


class SingleSpaceFormatter(AbstractFormatter):

    def format_text(self, matched_text, matched_setting):
        matched_text = matched_text.strip( " " )

        if matched_setting:
            return " " * matched_setting + matched_text + " " * matched_setting

        else:
            return matched_text


class Backend(pushdown.Interpreter):

    def __init__(self, formatter, tree, program, settings):
        super().__init__()
        self.tree = tree
        self.program = formatter( program, settings )

        ## A list of lists, where each list saves all the matches performed by
        ## the last match_statement on scope_name_statement
        self.last_match_stack = []

        ## This is set to False every push statement, and set to True, after
        ## every match statement. This way we can know whether there is a match
        ## statement after a push statement.
        self.is_there_push_after_match = False
        self.is_there_scope_after_match = False

        self.cached_includes = {}
        self.cache_includes( tree )

        self.visit( tree )
        log( 4, "Tree: \n%s", tree.pretty( debug=0 ) )

    def cache_includes(self, tree):
        log( 4, "tree.data: ", tree.data )

        for child in tree.children:

            if isinstance(child, Tree) and child.data == "miscellaneous_language_rules":
                include_name = child.children[0]
                include_tree = child.children[1]

                log( 4, "include_name: ", include_name )
                self.cached_includes[include_name] = include_tree

    def target_language_name_statement(self, tree):
        target_language_name = tree.children[0]

        self.target_language_name = target_language_name
        log( 4, "target_language_name: %s", target_language_name )

    def master_scope_name_statement(self, tree):
        master_scope_name = tree.children[0]

        self.master_scope_name = master_scope_name
        log( 4, "master_scope_name: %s", master_scope_name )

    def include_statement(self, tree):
        include_statement = str( tree.children[0] )

        log( 4, "include_statement: %s", include_statement )
        self.visit_children( self.cached_includes[include_statement] )

    def miscellaneous_language_rules(self, tree):
        miscellaneous_language_rules = tree.children[0]
        log( 4, "miscellaneous_language_rules: %s", miscellaneous_language_rules )

    ## match_statement -> scope_name_statement -> push_statement ->
    ##                                                              match_statement -> pop_statement
    ##                                                              match_statement -> scope_name_statement -> pop_statement
    ##                                                              meta_scope_statement -> match_statement -> pop_statement
    def match_statement(self, tree):
        log( 4, "is_there_push_after_match: %s", self.is_there_push_after_match )

        ## Discards the last_match_stack because we do not need the stack when
        ## there are 2 matches consecutives without a new push
        if not self.is_there_push_after_match and self.last_match_stack:
            self.last_match_stack.pop()

        self.is_there_push_after_match = False
        self.is_there_scope_after_match = False
        match = tree.children[0]
        self.match = re.compile( str(match) )

        log( 4, "match: %s", self.match.pattern )
        # log( 4, "tree: %s", tree )
        self.visit_children( tree )

    def push_statement(self, tree):
        self.is_there_push_after_match = True
        log( 4, "push_stack: %s", self.last_match_stack )

        if not self.is_there_scope_after_match:
            self.last_match_stack.append( [ match for match in self.match.finditer( str(self.program) ) ] )
        # log( 4, "tree: %s", tree )
        self.visit_children( tree )

    def meta_scope_statement(self, tree):
        meta_scope = tree.children[0]
        self.meta_scope = meta_scope
        log( 4, "pattern: %s", self.match.pattern )
        log( 4, "meta_scope: %s", meta_scope )

    def pop_statement(self, tree):
        """ Used the saved self.meta_scope and self.last_match_stack to process the input program. """
        log( 4, "pop_statement: %s", self.meta_scope )
        log( 4, "last_match_stack: %s", self.last_match_stack )
        log( 4, "is_there_push_after_match: %s", self.is_there_push_after_match )
        log( 4, "is_there_scope_after_match: %s", self.is_there_scope_after_match )

        # When there is a scope_name_statement after a push_statement, it means that
        # the self.match regular expression was already evaluated, therefore, we
        # must to reuse the cached result on the top of the stack and ignore the
        # penultimate matches positions
        if not self.is_there_push_after_match and self.is_there_scope_after_match:
            last_matches = self.last_match_stack.pop()
            matches = self.last_match_stack.pop()
            reversed_matches = list( reversed( matches ) )

            for last_match in last_matches:
                self.program.add_meta_scope( str(self.meta_scope), reversed_matches, last_match, True )

        else:
            last_matches = self.last_match_stack.pop()
            reversed_last_matches = list( reversed( last_matches ) )

            for last_match in last_matches:
                match = self.match.search( str( self.program ), last_match.end(0) )
                # log( "match: '%s'", match )
                # log( "pattern: '%s' last_match.end", self.match.pattern, last_match.end(0) )

                if match is None:
                    log( 1, "Error: Could not find the pop end statement! Skipping highlighting... match '%s' pattern '%s' end '%s'",
                            match, self.match.pattern, last_match.end(0) )

                    match = last_match

                self.program.add_meta_scope( str(self.meta_scope), reversed_last_matches, match )

    def scope_name_statement(self, tree):
        """ Used the saved self.match to process the input program. """
        self.is_there_scope_after_match = True
        scope_name = tree.children[0]
        self.scope_name = scope_name

        log( 4, "pattern: %s", self.match.pattern )
        log( 4, "scope_name: %s", scope_name )
        self.last_match_stack.append([])
        self.match.sub( lambda match: self.program.add_match( str(scope_name),
                self.last_match_stack, match ), str( self.program ) )

    def generated_html(self):
        log( 4, "..." )
        document = [ get_html_header( "%s - %s" % ( self.target_language_name, self.master_scope_name ) ) ]

        for item in self.program.get_new_program():
            document.append( str(item) )

        document.append( get_html_footer() )
        return "".join( document )

