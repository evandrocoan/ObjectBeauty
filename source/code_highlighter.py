
import re
import pushdown
import yattag

from pushdown import Tree

from debug_tools import getLogger
from debug_tools.utilities import get_representation

log = getLogger(127, __name__)


class ParsedProgram(object):
    """
        Represents a program as chunks of data as (text_chunk_start_position,
        text_chunk).
    """

    def __init__(self, program, theme):
        super().__init__()
        self.initial_size = len( program )
        self.program = program
        self.theme = theme

        self.new_program = []
        log( 4, "program %s: `%s`", len( str( self.program ) ), self.program )

    def __str__(self):
        """
            Returns the current version of the program,
            after being cuted by add_match().
        """
        return self.program

    __repr__ = __str__

    def get_new_program(self):
        """
            Sorts the list of (text_chunk_start_position, text_chunk) accordingly to
            `text_chunk_start_position` and return the new program as full string.
        """
        fixed_program = sorted( self.new_program, key=lambda item: item[0] )
        fixed_program_len = len(fixed_program)

        # Copy the unmatched chunks of text into the final program on self.new_program
        for index in range( 0, fixed_program_len ):

            if index < fixed_program_len - 1:
                current_chunk = fixed_program[index]
                next_chunk = fixed_program[index+1]

                if current_chunk[1] < next_chunk[0]:
                    self.new_program.append( ( current_chunk[1], next_chunk[0], self.program[current_chunk[1]:next_chunk[0]] ) )

            else:
                current_chunk = fixed_program[index]

                if current_chunk[1] < len( self.program ):
                    self.new_program.append( ( current_chunk[1], len( self.program ), self.program[current_chunk[1]:] ) )

        # At the end of the process, we must to preserve the program size on self.program
        # for the correct merge with the text chunks processed
        assert len( self.program ) == self.initial_size

        fixed_program = sorted( self.new_program, key=lambda item: item[0] )
        return "".join( [ item[2] for item in fixed_program ] )

    def get_theme(self, scope_name):
        program_scopes = scope_name.split( '.' )
        current_program_scope = ""
        latest_matched_color = ""

        for program_scope in program_scopes:
            current_program_scope += program_scope

            for theme_scope_name, theme_color in self.theme.items():
                current_theme_scope = ""
                theme_scopes = theme_scope_name.split( '.' )

                for theme_scope in theme_scopes:
                    current_theme_scope += theme_scope

                    if current_theme_scope == current_program_scope:
                        latest_matched_color = theme_color

        return latest_matched_color

    def add_match(self, scope_name, match):
        log( 4, "match: %s", match )
        self.program = self.program[:match.start(0)] + " " * ( match.end(0) - match.start(0) ) + self.program[match.end(0):]
        doc, tag, text, line = yattag.Doc().ttl()

        with tag( 'font', color=self.get_theme(scope_name) ):
            text(match[0])

        formatted_text = doc.getvalue()
        self.new_program.append( ( match.start(0), match.end(0), formatted_text ) )

        log( 4, "program %s: `%s`", len( str( self.program ) ), self.program )
        log( 4, "formatted_text: %s", formatted_text )


class Backend(pushdown.Interpreter):

    def __init__(self, tree, program, theme):
        super().__init__()
        self.tree = tree
        self.program = ParsedProgram( program, theme )
        self.doc, self.tag, self.text, self.line = yattag.Doc().ttl()

        self.visit( tree )
        log( 4, "Tree: \n%s", tree.pretty( debug=0 ) )

    def target_language_name_statement(self, tree):
        target_language_name = tree.children[0]

        self.target_language_name = target_language_name
        log( 4, "target_language_name: %s", target_language_name )

    def master_scope_name_statement(self, tree):
        master_scope_name = tree.children[0]

        self.master_scope_name = master_scope_name
        log( 4, "master_scope_name: %s", master_scope_name )

    def match_statement(self, tree):
        match = tree.children[0]
        self.match = re.compile( str(match) )

        log( 4, "match: %s", self.match.pattern )
        log( 4, "tree: %s", tree )
        self.visit_children( tree )

    def scope_name(self, tree):
        scope_name = tree.children[0]

        log( 4, "pattern: %s", self.match.pattern )
        log( 4, "scope_name: %s", scope_name )
        self.match.sub( lambda match: self.program.add_match(str(scope_name), match), str( self.program ) )

    def generated_html(self):
        log( 4, "..." )
        log( 4, "program_parsed %s: `%s`", len( str( self.program ) ), self.program )
        log( 4, "new_program: %s", self.program.new_program )
        log( 4, "new_program_parsed: %s", self.program.get_new_program() )

        with self.tag('html'):
            with self.tag('body'):
                self.doc.asis( self.program.get_new_program() )

        return yattag.indent( self.doc.getvalue() )

