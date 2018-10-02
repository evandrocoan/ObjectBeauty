#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Licensing
#
# Unit Tests Utilities
# Copyright (C) 2018 Evandro Coan <https://github.com/evandrocoan>
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

import os
import difflib
import unittest

from debug_tools import getLogger
log = getLogger( 127, __name__ )


class TestingUtilities(unittest.TestCase):
    """
        Holds common features across all Unit Tests.
    """

    def setUp(self):
        """
            Called right before each Unit Test is ran, to setup new setting values.
        """

        ## Set the maximum size of the assertion error message when Unit Test fail
        self.maxDiff = None

    def assertTextEqual(self, goal, results):
        """
            Remove both input texts indentation and trailing white spaces, then assertEquals() both
            of the inputs.
        """
        goal = wrap_text( goal, trim_tabs=True, trim_spaces=True )
        results = wrap_text( results, trim_tabs=True, trim_spaces=True )

        # print( goal.encode( 'ascii' ) )
        # print( results.encode( 'ascii' ) )
        # self.unidiff_output( goal, results )
        self.assertEqual( goal, results )

    def assertRaisesRegex(self, exception, results):
        """
            Remove both input texts indentation and trailing white spaces, then assertEquals() both
            of the inputs.
        """
        results = wrap_text( results, trim_tabs=True, trim_spaces=True )
        super().assertRaisesRegex( exception, results )

    def unidiff_output(self, expected, actual):
        """
            Helper function. Returns a string containing the unified diff of two multiline strings.
            https://stackoverflow.com/questions/845276/how-to-print-the-comparison-of-two-multiline-strings-in-unified-diff-format
            https://stackoverflow.com/questions/15864641/python-difflib-comparing-files
            https://stackoverflow.com/questions/32359402/comparison-of-multi-line-strings-in-python-unit-test
        """
        expected = expected.splitlines( 1 )
        actual = actual.splitlines( 1 )

        # diff = difflib.ndiff( expected, actual )
        if expected != actual:
            diff = difflib.context_diff( expected, actual, fromfile='expected input', tofile='actual output', lineterm='\n' )
            self.fail( '\n' + ''.join( diff ) )


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

#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Licensing
#
# Project Utilities
# Copyright (C) 2018 Evandro Coan <https://github.com/evandrocoan>
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

import os
import re

import time
import random

import lark
import textwrap

from natsort import natsorted
from debug_tools import getLogger

log = getLogger( 127, __name__ )

# An unique identifier for any created object
initial_hash = random.getrandbits( 32 )


def get_unique_hash():
    """
        Generates an unique identifier which can be used to uniquely identify distinct object
        instances.
    """
    global initial_hash

    initial_hash += 1
    return initial_hash


def get_relative_path(relative_path, script_file):
    """
        Computes a relative path for a file on the same folder as this class file declaration.
        https://stackoverflow.com/questions/4381569/python-os-module-open-file-above-current-directory-with-relative-path
    """
    basepath = os.path.dirname( script_file )
    filepath = os.path.abspath( os.path.join( basepath, relative_path ) )
    return filepath


def assure_existing_key(dictionary, key, default_value):
    """
        If the given `key` is not present on the `dictionary`, then add it with the `default_value`.
    """

    if key not in dictionary:
        dictionary[key] = default_value


def get_duplicated_elements(elements_list):
    """
        Given an `elements_list` with duplicated elements, return a set only with the duplicated
        elements in the list. If there are not duplicated elements, an empty set is returned.
        How do I find the duplicates in a list and create another list with them?
        https://stackoverflow.com/questions/9835762/how-do-i-find-the-duplicates-in-a-list-and-create-another-list-with-them
    """
    visited_elements = set()
    visited_and_duplicated = set()

    add_item_to_visited_elements = visited_elements.add
    add_item_to_visited_and_duplicated = visited_and_duplicated.add

    for item in elements_list:

        if item in visited_elements:
            add_item_to_visited_and_duplicated(item)

        else:
            add_item_to_visited_elements(item)

    return visited_and_duplicated


def emquote_string(string):
    """
        Return a string escape into single or double quotes accordingly to its contents.
    """
    string = str( string )
    is_single = "'" in string
    is_double = '"' in string

    if is_single and is_double:
        return '"{}"'.format( string.replace( "'", "\\'" ) )

    if is_single:
        return '"{}"'.format( string )

    return "'{}'".format( string )


def sort_dictionary_lists(dictionary):
    """
        Give a dictionary, call `sorted` on all its elements.
    """

    for key, value in dictionary.items():
        dictionary[key] = sorted( value )

    return dictionary


def sort_alphabetically_and_by_length(iterable):
    """
        Give an `iterable`, sort its elements accordingly to the following criteria:
            1. Sorts normally by alphabetical order
            2. Sorts by descending length
        How to sort by length of string followed by alphabetical order?
        https://stackoverflow.com/questions/4659524/how-to-sort-by-length-of-string-followed-by-alphabetical-order
    """
    return sorted( sorted( natsorted( iterable, key=lambda item: str( item ).lower() ),
                          key=lambda item: str( item ).istitle() ),
                  key=lambda item: len( str( item ) ) )


def sort_correctly(iterable):
    """
        Sort the given iterable in the way that humans expect.
        How to sort alpha numeric set in python
        https://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
    """
    convert = lambda text: int( text ) if text.isdigit() else text
    alphanum_key = lambda key: [convert( characters ) for characters in re.split( '([0-9]+)', str( key ).lower() )]
    return sorted( sorted( iterable, key=alphanum_key ), key=lambda item: str( item ).istitle() )


def get_largest_item_size(iterable):
    """
        Given a iterable, get the size/length of its largest key value.
    """
    largest_key = 0

    for key in iterable:

        if len( key ) > largest_key:
            largest_key = len( key )

    return largest_key


def dictionary_to_string(dictionary):
    """
        Given a dictionary with a list for each string key, call `sort_dictionary_lists()` and
        return a string representation by line of its entries.
    """

    if not len( dictionary ):
        return " No elements found."

    strings = []
    elements_strings = []

    dictionary = sort_dictionary_lists( dictionary )
    largest_key = get_largest_item_size( dictionary.keys() ) + 1

    for key, values in dictionary.items():
        elements_strings.clear()

        for item in values:
            elements_strings.append( "{}".format( str( item ) ) )

        strings.append( "{:>{largest_key}}: {}".format( str( key ), " ".join( elements_strings ),
                largest_key=largest_key ) )

    return "\n".join( strings )


def convert_to_text_lines(iterable, use_repr=True, new_line=True, sort=None):
    """
        Given a dictionary with a list for each string key, call `sort_dictionary_lists()` and
        return a string representation by line of its entries.
    """

    if isinstance( iterable, dict):
        return dictionary_to_string( iterable )

    if not iterable:
        return " No elements found."

    strings = []

    if sort:
        iterable = sort( iterable )

    else:
        iterable = sort_alphabetically_and_by_length( iterable )

    for item in iterable:
        strings.append( " {}".format( repr( item ) ) )

    return ( "\n" if new_line else "" ).join( strings )


def getCleanSpaces(inputText, minimumLength=0, lineCutTrigger="", keepSpaceSepators=False):
    """
        Removes spaces and comments from the input expression.
        `minimumLength` of a line to not be ignored
        `lineCutTrigger` all lines after a line starting with this string will be ignored
        `keepSpaceSepators` if True, it will keep at a single space between sentences as `S S`, given `S    S`
    """

    if keepSpaceSepators:
        removeNewSpaces = ' '.join( inputText.split( ' ' ) )
        lineCutTriggerNew = ' '.join( lineCutTrigger.split( ' ' ) ).strip( ' ' )

    else:
        removeNewSpaces = re.sub( r"\t| ", "", inputText )
        lineCutTriggerNew = re.sub( r"\t| ", "", lineCutTrigger )

    # log( 1, "%s", inputText, minimumLength=0 )
    lines = removeNewSpaces.split( "\n" )
    clean_lines = []

    for line in lines:

        if keepSpaceSepators:
            line = line.strip( ' ' )

        if minimumLength:

            if len( line ) < minimumLength:
                continue

        if lineCutTrigger:

            if line.startswith( lineCutTriggerNew ):
                break

        if line.startswith( "#" ):
            continue

        clean_lines.append( line )

    return clean_lines


def wrap_text(text, wrap=0, trim_tabs=False, trim_spaces=False, trim_lines=False, indent=""):
    """
        1. Remove input text leading common indentation, trailing white spaces
        2. If `wrap`, wraps big lists on 80 characters.
        3. If `trim_spaces`, remove leading '+' symbols and if `trim_tabs` replace tabs with 2 spaces.
        4. If `trim_lines`, remove all new line characters.
    """
    clean_lines = []

    if not isinstance( text, str ):
        text = str( text )

    if trim_tabs:
        text = text.replace( '\t', '  ' )

    dedent_lines = textwrap.dedent( text ).strip( '\n' )

    if trim_spaces:

        for line in dedent_lines.split( '\n' ):
            line = line.rstrip( ' ' ).lstrip( '+' )
            clean_lines.append( line )

        dedent_lines = textwrap.dedent( "\n".join( clean_lines ) )

    if wrap:
        clean_lines.clear()

        for line in dedent_lines.split( '\n' ):
            line = textwrap.fill( line, width=wrap, subsequent_indent=indent )
            clean_lines.append( line )

        dedent_lines = "\n".join( clean_lines )

    if trim_lines:
        dedent_lines = "".join( dedent_lines.split( '\n' ) )

    return dedent_lines


def get_representation(self, ignore=[], emquote=False):
    """
        Given a object, iterating through all its public attributes and return then as a string
        representation.
        `ignore` a list of attributes to be ignored
        `emquote` if True, puts the attributes values inside single or double quotes accordingly.
    """
    valid_attributes = self.__dict__.keys()
    clean_attributes = []

    if emquote:

        def pack_attribute(string):
            return emquote_string( string )

    else:

        def pack_attribute(string):
            return string

    for attribute in valid_attributes:

        if not attribute.startswith( '_' ) and attribute not in ignore:
            clean_attributes.append( "{}: {}".format( attribute, pack_attribute( self.__dict__[attribute] ) ) )

    return "%s %s;" % ( self.__class__.__name__, ", ".join( clean_attributes ) )


