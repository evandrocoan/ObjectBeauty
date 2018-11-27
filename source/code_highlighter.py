
import re
import pprint
import pushdown
import dominate

from pushdown import Tree
from collections import OrderedDict

from debug_tools import getLogger
from debug_tools.utilities import get_representation

log = getLogger(1, __name__)


class ParsedProgram(object):
    """
        Represents a program as chunks of data as (text_chunk_start_position,
        text_chunk).
    """

    def __init__(self, program, theme):
        super().__init__()
        self.initial_size = len( program )
        self.program = program
        self.theme = OrderedDict( sorted( theme.items(), key=lambda item: len( str( item ) ) ) )

        self.new_program = []
        self.cached_new_program = []
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
                    doc = self._get_div_doc( self.program[current_chunk[1]:next_chunk[0]] )
                    self.new_program.append( ( current_chunk[1], next_chunk[0], doc ) )

            else:
                current_chunk = fixed_program[index]

                if current_chunk[1] < len( self.program ):
                    doc = self._get_div_doc( self.program[current_chunk[1]:] )
                    self.new_program.append( ( current_chunk[1], len( self.program ), doc ) )

        # At the end of the process, we must to preserve the program size on self.program
        # for the correct merge with the text chunks processed
        assert len( self.program ) == self.initial_size, "Expected %s got %s" % ( self.initial_size, len(self.program) )
        fixed_program = sorted( self.new_program, key=lambda item: item[0] )
        fixed_program_len = len(fixed_program)

        # for index in range( 0, fixed_program_len - 1 ):
        #     current_chunk = fixed_program[index]
        #     next_chunk = fixed_program[index+1]

        #     if current_chunk[1] > next_chunk[0]:
        #         fixed_program[index], fixed_program[index+1] = fixed_program[index+1], fixed_program[index]

        log( 4, "fixed_program:\n%s", pprint.pformat( [( item[0], item[1], str(item[2]) )for item in fixed_program], indent=2, width=200 ) )
        log( 4, "cached_new_program: %s", self.cached_new_program )

        self.cached_new_program = [ item[2] for item in fixed_program ]
        return self.cached_new_program

    def _get_div_doc(self, input_text):
        doc = dominate.tags.span( grammar_scope="none", theme_scope="none" )
        with doc:
            self._add_doc_text( input_text )
        return doc

    def _add_doc_text(self, input_text):
        dominate.util.raw( dominate.util.escape( input_text ).replace("\n", "<br />" ) )

    def get_theme(self, scope_name):
        program_scopes = scope_name.split( '.' )

        def select():
            for index in range( len(program_scopes), 0, -1 ):
                program_scope = ".".join( [program_scopes[inner_index] for inner_index in range( 0, index ) ] )

                for theme_scopes, theme_color in self.theme.items():
                    theme_scopes = theme_scopes.split( '.' )

                    for index in range( 1, len(theme_scopes) + 1 ):
                        theme_scope = ".".join( [theme_scopes[inner_index] for inner_index in range( 0, index ) ] )
                        # log( 4, "theme_color: %s, comparing `%s` with `%s`", theme_color, program_scope, theme_scope )

                        if theme_scope == program_scope:
                            # log( 4, "Selecting %s with %s", theme_scope, theme_color )
                            return theme_color, theme_scope

            return "", ""

        first_matched_color, theme_scope = select()

        # log( 4, "first_matched_color: %s", first_matched_color )
        return first_matched_color, theme_scope

    def add_match(self, scope_name, last_match_stack, match):
        log( 4, "add_match: %s", match )
        last_match_stack[-1].append(match)
        match_start = match.start(0)
        match_end = match.end(0)
        match_start, match_end = match_start, match_end

        self.program = self.program[:match_start] + "§" * ( match_end - match_start ) + self.program[match_end:]
        assert len( self.program ) == self.initial_size, "Expected %s got %s" % ( self.initial_size, len(self.program) )

        self._generate_chunk_html( scope_name, match[0], match_start, match_end )

    def add_meta_scope(self, scope_name, last_matches, match):
        log( 4, "add_meta_scope: %s", match )
        last_match = last_matches.pop() if last_matches else None
        match_end = match.end(0)

        if last_match:
            match_start = last_match.end(0)
            match_start, match_end = match_start, match_end

            self._generate_chunk_html( scope_name, self.program[match_start:match_end], match_start, match_end )
            self.program = self.program[:last_match.end(0)] + "§" * ( match.end(0) - last_match.end(0) ) + self.program[match.end(0):]

        else:
            match_start = match.start(0)
            match_start, match_end = match_start, match_end

            self.program = self.program[:match_start] + "§" * ( match_end - match_start ) + self.program[match_end:]
            self._generate_chunk_html( scope_name, matched_text, match_start, match_end )

        assert len( self.program ) == self.initial_size, "Expected %s got %s" % ( self.initial_size, len(self.program) )

    def _generate_chunk_html(self, grammar_scope, matched_text, match_start, match_end):
        first_matched_color, theme_scope = self.get_theme(grammar_scope)
        doc = dominate.tags.font( color=first_matched_color, grammar_scope=grammar_scope, theme_scope=theme_scope )

        with doc:
            self._add_doc_text( matched_text )

        self.new_program.append( ( match_start, match_end, doc ) )
        log( 4, "formatted_text: %s", str( doc ) )
        log( 4, "program %s: `%s`", len( str( self.program ) ), self.program )


class Backend(pushdown.Interpreter):

    def __init__(self, tree, program, theme):
        super().__init__()
        self.tree = tree
        self.program = ParsedProgram( program, theme )

        ## A list of lists, where each list saves all the matches performed by
        ## the last match_statement on scope_name_statement
        self.last_match_stack = []

        ## This is set to False every push statement, and set to True, after
        ## every match statement. This way we can know whether there is a match
        ## statement after a push statement.
        self.is_there_push_after_match = False
        self.is_there_scope_after_match = False

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

        if not self.is_there_push_after_match and self.is_there_scope_after_match:
            self.last_match_stack.pop()

        last_matches = self.last_match_stack.pop()
        reversed_last_matches = list( reversed( last_matches ) )

        for last_match in last_matches:
            match = self.match.search( str( self.program ), last_match.end(0) )
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
        doc = dominate.document( title="%s - %s" % ( self.target_language_name, self.master_scope_name ) )

        with doc:
            with dominate.tags.span( style="font-family: monospace;" ):
                for item in self.program.get_new_program():
                    doc.add( item )

        return str( doc )

