
import re
import lark

from lark import Tree, LarkError, Token

from debug_tools import getLogger
from debug_tools.utilities import get_representation

log = getLogger(__name__)


class SemanticErrors(LarkError):
    def __init__(self, warnings, errors):
        if warnings:
            self.warnings = self._build_messages(warnings)
        else:
            self.warnings = None

        if errors:
            self.errors = self._build_messages(errors)
        else:
            self.errors = None

    def _build_messages(self, exceptions):
        # https://stackoverflow.com/questions/16625068/combine-lists-by-joining-strings-with-matching-index-values
        messages = map( lambda a, b: "%s. %s" % (a, b), range( 1, len(exceptions) + 1 ), exceptions )
        return "\n".join( message for message in messages )

    def __str__(self):
        return ( "\n%s\n" % self.errors if self.errors else "" ) + \
                ( "\n  Warnings:\n%s" % self.warnings if self.warnings else "" )


class UndefinedInput(object):

    def __init__(self):
        super(UndefinedInput, self).__init__()
        self.str = ""

    def resolve(self, value):
        raise NotImplementedError( "%s is an abstract class" % self.__name__ )

    def __repr__(self):

        if self.str:
            return self.str

        return get_representation(self)

    def __str__(self):

        if self.str:
            return self.str

        else:
            return self.__repr__()


class VariableUsage(UndefinedInput):
    """
        Represents a variable which is used somewhere, but its definition is yet unknown.

        As soon as this variable definition is know, this object will return the
        variable complete representation.
    """
    def __init__(self, name, token):
        super(VariableUsage, self).__init__()
        self.name = name
        self.token = token

    def resolve(self, value):

        if self.str:
            return False

        self.str = str( value )
        return True


class VariableDeclaration(UndefinedInput):

    def __init__(self, tokens, token):
        super(VariableDeclaration, self).__init__()
        self.tokens = tokens
        self.token = token

    def resolve(self, definitions):
        """
            @param `definitions` a dictionary with all completely know
                variables. For example { "$varrrr:" : " varrrr " }
        """

        if self.str:
            return False

        resolutions = []

        for token in self.tokens:

            if token.type == 'variable_usage':
                variable_body = definitions[str( token )]

                if variable_body.str:
                    resolutions.append( str( variable_body ) )

                else:
                    log('The variable definition is not yet complete')
                    return False

            else:
                resolutions.append( str( token ) )

        self.str = "".join(resolutions)
        return True


class InputString(UndefinedInput):

    def __init__(self, tokens, definitions):
        super(InputString, self).__init__()
        self.tokens = tokens
        self.definitions = definitions

    def __str__(self):
        """
            @param `definitions` a dictionary with all completely know
                variables. For example { "$varrrr:" : " varrrr " }
        """

        resolutions = []
        # log( 1, 'self.definitions %s', self.definitions )

        for token in self.tokens:
            # log( 1, 'token %s', token )

            if isinstance( token, VariableUsage ):
                variable_name = token.name
                # log(1, 'variable_name %s', variable_name )
                resolutions.append( str( self.definitions[variable_name] ) )

            elif isinstance( token, Tree ):
                variable_name = token.children[0]
                # log(1, 'variable_name %s', variable_name )
                resolutions.append( str( self.definitions[variable_name] ) )

            else:
                resolutions.append( str( token ) )

        return "".join( resolutions )


class TreeTransformer(lark.Transformer):
    """
        Transforms the Derivation Tree nodes into meaningful string representations,
        allowing simple recursive parsing parsing and conversion to Abstract Syntax Tree.
    """

    def __init__(self):
        ## Saves all the semantic errors errors detected so far
        self.errors = []

        ## Saves all warnings noted so far
        self.warnings = []

        ## Whether the mandatory/obligatory global scope name statement was declared
        self.is_master_scope_name_set = False

        ## Whether the mandatory/obligatory global language name statement was declared
        self.is_target_language_name_set = False

        ## Can only be one scope called `contexts`
        self.has_called_language_construct_rules = False

        ## Pending variables declarations
        self.used_variables = {}

        ## Pending variables usages
        self.defined_variables = {}

        ## A list of miscellaneous_language_rules include contexts defined for duplication checking
        self.defined_includes = {}

        ## A list of required includes to check for missing includes
        self.required_includes = {}
        self.pending_match_statements = []

    def language_syntax(self, tree, children):
        """
            This is the grammar start symbol and will be called by last with all
            partial subtrees the start symbol derivates.

            This is a great place to check whether global grammar properties
            where set.
        """

        if not self.has_called_language_construct_rules:
            self.errors.append( "You must to define the `contexts` block in your grammar!" )

        self._resolve_variables_definitions()
        self._check_includes_definitions()
        self._check_for_main_rules()

        if self.errors or self.warnings:
            # log('tree\n', children[1].pretty())
            raise SemanticErrors(self.warnings, self.errors)

        return self.__default__(tree.data, children, tree.meta)

    def language_construct_rules(self, tree, children):
        self.has_called_language_construct_rules = True
        return self.__default__(tree.data, children, tree.meta)

    def miscellaneous_language_rules(self, tree, children):
        first_token = tree.children[0]
        include_name = str(first_token)
        assert tree.data == 'miscellaneous_language_rules', "Just documenting what the data attribute has."
        assert isinstance( first_token, Token ), "The first children must be a Token, while the second is a subtree."

        if include_name in self.defined_includes:
            self.errors.append( "Duplicated include `%s` defined in your grammar on %s" % ( include_name, first_token.pretty() ) )

        if include_name == 'contexts':
            self.errors.append( "Extra `contexts` rule defined in your grammar on %s" % first_token.pretty() )

        else:
            self.defined_includes[include_name] = first_token

        return self.__default__(tree.data, children, tree.meta)

    def target_language_name_statement(self, tree, children):
        first_token = tree.children[0].children[0]
        if self.is_target_language_name_set:
            self.errors.append( "Duplicated target language name defined in your grammar on %s" % ( first_token.pretty() ) )

        self.is_target_language_name_set = True
        return self.__default__(tree.data, children, tree.meta)

    def master_scope_name_statement(self, tree, children):
        first_token = tree.children[0].children[0]
        if self.is_master_scope_name_set:
            self.errors.append( "Duplicated master scope name defined in your grammar on %s" % ( first_token.pretty() ) )

        self.is_master_scope_name_set = True
        return self.__default__(tree.data, children, tree.meta)

    def include_statement(self, tree, children):
        first_token = tree.children[0].children[0]
        include_name = str(first_token)

        self.required_includes[include_name] = first_token
        return self.__default__(tree.data, children, tree.meta)

    def variable_declaration(self, tree, children):
        # log(1, 'tree: \n%s', tree.pretty(debug=1))
        # log(1, 'children: \n%s', tree.children)
        children = tree.children

        # [
        #   Tree(variable_name, [Token(__ANON_2, '$variable:')]),
        #   [
        #       Token(__ANON_3, ' test'),
        #       Token(VARIABLE_USAGE, '$varrrr:'),
        #       Token(__ANON_4, 'test')
        #   ]
        # ]
        variable_name = str( children[0] )
        variable_body = children[1].children
        input_string = VariableDeclaration( variable_body, children[0] )

        # Trim trailing obligatory white space by the grammar
        variable_name = variable_name[:-1]

        # log( 'variable_name:', variable_name )
        # log( 'variable_body:', variable_body )
        # log( input_string )

        self.defined_variables[variable_name] = input_string
        return input_string

    def variable_usage(self, tree, children):
        children = tree.children
        variable_name = str( children[0] )

        undefined_variable = VariableUsage( variable_name, children[0] )
        self.used_variables[variable_name] = undefined_variable

        # log( 'variable_name:', variable_name )
        # log( undefined_variable )

        # log(1, 'tree: \n%s', tree.pretty(debug=1))
        return undefined_variable

    def match_statement(self, tree, children):
        include_name = children[0]
        # log('include_name', type(include_name))

        self.pending_match_statements.append( include_name )
        return self.__default__(tree.data, children, tree.meta)

    def free_input_string(self, tree, children):
        # log(1, 'tree: \n%s', tree.pretty(debug=1))
        # log(1, 'children: \n%s', tree.children)

        # Tree
        # (
        #   free_input_string,
        #   [
        #       Token(TEXT_CHUNK_END, 'source.sma')
        #   ]
        # )
        variable_body = children
        input_string = InputString( variable_body, self.defined_variables )

        # log( 'variable_body:', variable_body )
        # log( input_string )
        return input_string

    def _check_for_main_rules(self):
        """
            Look for missing required main rules on the grammar preamble statement.
        """
        if not self.is_master_scope_name_set:
            self.errors.append( "Missing master scope name in your grammar preamble." )

        if not self.is_target_language_name_set:
            self.errors.append( "Missing target language name in your grammar preamble." )

        # log.newline()
        for include_name in self.pending_match_statements:
            # log('include_name', type(include_name))
            # log('include_name', include_name)

            try:
                re.compile(str(include_name))

            except re.error as error:
                self.errors.append( "Invalid regular expression `%s` on match statement: %s" % ( include_name, error) )

    def _check_includes_definitions(self):
        """
            Resolve all pending include usages across the tree.
        """
        # Look for missing required main rules on the grammar preamble statement.
        for include_name, include_token in self.defined_includes.items():
            if include_name not in self.required_includes:
                self.warnings.append( "Unused include `%s` defined in your grammar on %s" % ( include_name, include_token.pretty() ) )

        # Look for missing required includes by the `include` statement.
        for include_name, include_token in self.required_includes.items():
            if include_name not in self.defined_includes:
                self.errors.append( "Missing include `%s` defined in your grammar on %s" % ( include_name, include_token.pretty() ) )

    def _resolve_variables_definitions(self):
        """
            Resolve all pending variable usages across the tree.
        """

        # Checks for undefined variables usage
        for name, variable in self.used_variables.items():
            if name not in self.defined_variables:
                self.errors.append( "Missing variable `%s` defined in your grammar on %s" % ( name, variable.token.pretty(1) ) )

        # Checks for unused variables
        for name, variable in self.defined_variables.items():
            # log(1, 'name %s', name)
            if name not in self.used_variables:
                self.warnings.append( "Unused variable `%s` defined in your grammar on %s" % ( name, variable.token.pretty() ) )

        revolved_count = 1
        last_resolution = 0
        pending = {}
        resolved_variables = {}

        # work resolve variables usages on `self.used_variables` until it there is no new progress
        while revolved_count != last_resolution:
            # log('revolved_count', revolved_count, ', last_resolution', last_resolution)
            revolved_count = last_resolution
            just_resolved = []

            # Updates all variables definitions with the variables contents values
            for name, variable in self.defined_variables.items():
                # log( 1, 'Trying to resolve name %s, variable %s', name, variable )
                if variable.resolve( self.used_variables ):
                    # log( 1, 'Resolved variable to %s', variable )
                    just_resolved.append(name)
                    resolved_variables[name] = variable

            # When a defined_variables has inner unresolved variables, it can only be resolved later
            for variable in just_resolved:
                # log( 1, 'Deleting just resolved %s, value %s', variable, self.defined_variables[variable] )
                del self.defined_variables[variable]

            # Resolve all pending variables
            for name, variable in self.used_variables.items():
                # log( 1, 'Trying to resolve pending name %s, variable %s', name, variable )
                if name in resolved_variables:
                    resolution = resolved_variables[name]

                    if variable.resolve( resolution.str ):
                        # log( 1, 'Resolved variable to %s', variable )
                        last_resolution += 1

        # log.newline()
        # log(1, 'used_variables %s', self.used_variables)
        # log(1, 'resolved_variables %s', resolved_variables)

        # if the resolution count does not reach 0, something went wrong
        if len( self.defined_variables ) > 0:
            self.errors.append( "The following variables could be resolved:\n   `%s`" % ( self.defined_variables ) )

        self.defined_variables.update( resolved_variables )

    def _call_userfunc(self, tree, new_children=None):
        """
            Overrides the default behavior of TreeTransformer, to send the whole
            three to its children instead of only trees children.
        """
        # Assumes tree is already transformed
        children = tree.children if new_children is None else new_children
        try:
            f = getattr(self, tree.data)
        except AttributeError:
            return self.__default__(tree.data, children, tree.meta)
        else:
            return f(tree, children)
