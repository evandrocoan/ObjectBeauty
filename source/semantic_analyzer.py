
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


class ConstantUsage(UndefinedInput):
    """
        Represents a constant which is used somewhere, but its definition is yet unknown.

        As soon as this constant definition is know, this object will return the
        constant complete representation.
    """
    def __init__(self, name, token):
        super(ConstantUsage, self).__init__()
        self.name = name
        self.token = token

    def resolve(self, value):

        if self.str:
            return False

        self.str = str( value )
        return True


class ConstantDefinition(UndefinedInput):

    def __init__(self, tokens, token):
        super(ConstantDefinition, self).__init__()
        self.tokens = tokens
        self.token = token
        # log(1, 'token: %s', type(token))
        # log(1, 'token: %s', token)

    def resolve(self, definitions):
        """
            @param `definitions` a dictionary with all completely know
                constants. For example { "$varrrr:" : " varrrr " }
        """

        if self.str:
            return False

        resolutions = []

        for token in self.tokens:

            if token.type == 'constant_usage':
                constant_body = definitions[str( token )]

                if constant_body.str:
                    resolutions.append( str( constant_body ) )

                else:
                    log('The constant definition is not yet complete')
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

    def __getitem__(self, index):
        return self.tokens[index]

    def __str__(self):
        """
            @param `definitions` a dictionary with all completely know
                constants. For example { "$varrrr:" : " varrrr " }
        """

        resolutions = []
        # log( 1, 'self.definitions %s', self.definitions )

        for token in self.tokens:
            # log( 1, 'token %s', token )

            if isinstance( token, ConstantUsage ):
                constant_name = token.name
                # log(1, 'constant_name %s', constant_name )
                resolutions.append( str( self.definitions[constant_name] ) )

            elif isinstance( token, Tree ):
                constant_name = token.children[0]
                # log(1, 'constant_name %s', constant_name )
                resolutions.append( str( self.definitions[constant_name] ) )

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

        ## Pending constants declarations
        self.constant_usages = {}

        ## Pending constants usages
        self.constant_definitions = {}

        ## A list of miscellaneous_language_rules include contexts defined for duplication checking
        self.defined_includes = {}

        ## A list of required includes to check for missing includes
        self.required_includes = {}

        ## A list of regular expressions used on match statements,
        ## for validation when the constants definitions are completely know
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

        self._resolve_constants_definitions()
        self._check_includes_definitions()
        self._check_for_main_rules()

        if self.errors or self.warnings:
            # log('tree\n', children[1].pretty())
            raise SemanticErrors(self.warnings, self.errors)

        return self.__default__(tree, children)

    def language_construct_rules(self, tree, children):
        self.has_called_language_construct_rules = True
        return self.__default__(tree, children)

    def miscellaneous_language_rules(self, tree, children):
        first_token = children[0]
        include_name = str(first_token)
        assert tree.data == 'miscellaneous_language_rules', "Just documenting what the data attribute has."
        assert isinstance( first_token, Token ), "The first children must be a Token, while the second is a subtree."

        if include_name in self.defined_includes:
            self.errors.append( "Duplicated include `%s` defined in your grammar on %s" % ( include_name, first_token.pretty() ) )

        if include_name == 'contexts':
            self.errors.append( "Extra `contexts` rule defined in your grammar on %s" % first_token.pretty() )

        else:
            self.defined_includes[include_name] = first_token

        return self.__default__(tree, children)

    def target_language_name_statement(self, tree, children):
        input_string = children[0]
        # log(1, 'tree: \n%s', tree)
        # log(1, 'children: %s', children)
        # log(1, 'input_string: %s', type(input_string))
        # log(1, 'input_string: %s', input_string)
        if self.is_target_language_name_set:
            self.errors.append( "Duplicated target language name defined in your grammar on %s" % ( input_string[0].pretty() ) )

        self.is_target_language_name_set = True
        return self.__default__(tree, children)

    def master_scope_name_statement(self, tree, children):
        input_string = children[0]
        if self.is_master_scope_name_set:
            self.errors.append( "Duplicated master scope name defined in your grammar on %s" % ( input_string[0].pretty() ) )

        self.is_master_scope_name_set = True
        return self.__default__(tree, children)

    def include_statement(self, tree, children):
        input_string = children[0]
        include_name = str(input_string)

        self.required_includes[include_name] = input_string
        return self.__default__(tree, children)

    def constant_definition(self, tree, children):
        # log(1, 'tree: \n%s', tree.pretty(debug=1))
        # log(1, 'children: \n%s', tree.children)
        token = children[0]

        # [
        #   Tree(constant_name, [Token(CONSTANT_NAME_, '$constant:')]),
        #   [
        #       Token(TEXT_CHUNK, ' test'),
        #       Token(CONSTANT_USAGE_, '$varrrr:'),
        #       Token(TEXT_CHUNK_END, 'test')
        #   ]
        # ]
        constant_name = str( children[0] )
        constant_body = children[1]
        input_string = ConstantDefinition( constant_body, token )

        # Trim trailing obligatory white space by the grammar
        constant_name = constant_name[:-1]

        # log( 'constant_name:', constant_name )
        # log( 'constant_body:', constant_body )
        # log( input_string )

        if constant_name in self.constant_definitions:
            self.errors.append( "Constant redefinition on %s" % ( token.pretty() ) )

        self.constant_definitions[constant_name] = input_string
        return input_string

    def constant_usage(self, tree, children):
        token = children[0]
        constant_name = str( children[0] )

        undefined_constant = ConstantUsage( constant_name, children[0] )
        self.constant_usages[constant_name] = undefined_constant

        # log( 'constant_name:', constant_name )
        # log( undefined_constant )

        # log(1, 'tree: \n%s', tree.pretty(debug=1))
        return undefined_constant

    def match_statement(self, tree, children):
        include_name = children[0]
        # log('include_name', type(include_name))

        self.pending_match_statements.append( include_name )
        return self.__default__(tree, children)

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
        constant_body = children
        input_string = InputString( constant_body, self.constant_definitions )

        # log( 'constant_body:', constant_body )
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
                self.errors.append( "Missing include `%s` defined in your grammar on %s" % ( include_name, include_token[0].pretty() ) )

    def _resolve_constants_definitions(self):
        """
            Resolve all pending constant usages across the tree.
        """

        # Checks for undefined constants usage
        for name, constant in self.constant_usages.items():
            if name not in self.constant_definitions:
                self.errors.append( "Missing constant `%s` defined in your grammar on %s" % ( name, constant.token.pretty(1) ) )

        # Checks for unused constants
        for name, constant in self.constant_definitions.items():
            # log(1, 'name %s', name)
            if name not in self.constant_usages:
                self.warnings.append( "Unused constant `%s` defined in your grammar on %s" % ( name, constant.token.pretty() ) )

        revolved_count = 1
        last_resolution = 0
        pending = {}
        resolved_constants = {}

        # work resolve constants usages on `self.constant_usages` until it there is no new progress
        while revolved_count != last_resolution:
            # log('revolved_count', revolved_count, ', last_resolution', last_resolution)
            revolved_count = last_resolution
            just_resolved = []

            # Updates all constants definitions with the constants contents values
            for name, constant in self.constant_definitions.items():
                # log( 1, 'Trying to resolve name %s, constant %s', name, constant )
                if constant.resolve( self.constant_usages ):
                    # log( 1, 'Resolved constant to %s', constant )
                    just_resolved.append(name)
                    resolved_constants[name] = constant

            # When a constant_definitions has inner unresolved constants, it can only be resolved later
            for constant in just_resolved:
                # log( 1, 'Deleting just resolved %s, value %s', constant, self.constant_definitions[constant] )
                del self.constant_definitions[constant]

            # Resolve all pending constants
            for name, constant in self.constant_usages.items():
                # log( 1, 'Trying to resolve pending name %s, constant %s', name, constant )
                if name in resolved_constants:
                    resolution = resolved_constants[name]

                    if constant.resolve( resolution.str ):
                        # log( 1, 'Resolved constant to %s', constant )
                        last_resolution += 1

        # log.newline()
        # log(1, 'constant_usages %s', self.constant_usages)
        # log(1, 'resolved_constants %s', resolved_constants)

        # if the resolution count does not reach 0, something went wrong
        if len( self.constant_definitions ) > 0:
            self.errors.append( "The following constants could be resolved:\n   `%s`" % ( self.constant_definitions ) )

        self.constant_definitions.update( resolved_constants )

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
            return self.__default__(tree, children)
        else:
            return f(tree, children)

