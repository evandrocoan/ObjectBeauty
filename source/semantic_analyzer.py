
import re
import lark

from lark import Tree, LarkError, Token

from debug_tools import getLogger
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
        return ( self.errors if self.errors else "" ) + \
                ( "\n\n  Warnings:\n%s" % self.warnings if self.warnings else "" )


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

        self.is_master_scope_name_set = False
        self.is_target_language_name_set = False

        ## Can only be one scope called `contexts`
        self.has_called_language_construct_rules = False

        ## A list of miscellaneous_language_rules include contexts defined for duplication checking
        self.defined_includes = {}

        ## A list of required includes to check for missing includes
        self.required_includes = {}

    def language_syntax(self, tree):
        """
            This is the grammar start symbol and will be called by last with all
            partial subtrees the start symbol derivates.

            This is a great place to check whether global grammar properties
            where set.
        """

        if not self.has_called_language_construct_rules:
            self.errors.append( "You must to define the `contexts` block in your grammar!" )

        self._check_for_missing_includes()
        self._check_for_main_rules()
        self._check_for_unused_includes()

        if self.errors or self.warnings:
            raise SemanticErrors(self.warnings, self.errors)

        return self.__default__(tree.data, tree.children, tree.meta)

    def language_construct_rules(self, tree):
        self.has_called_language_construct_rules = True
        return self.__default__(tree.data, tree.children, tree.meta)

    def miscellaneous_language_rules(self, tree):
        first_token = tree.children[0]
        include_name = str(first_token)
        assert tree.data == 'miscellaneous_language_rules', "Just documenting what the data attribute has."
        assert isinstance( first_token, Token ), "The first children must be a Token, while the second is a subtree."

        if include_name in self.defined_includes:
            self.errors.append( "Duplicated include `%s` defined in your grammar on: %s" % ( include_name, first_token.pretty() ) )

        if include_name == 'contexts':
            self.errors.append( "Extra `contexts` rule defined in your grammar on: %s" % first_token.pretty() )

        else:
            self.defined_includes[include_name] = first_token

        return self.__default__(tree.data, tree.children, tree.meta)

    def target_language_name_statement(self, tree):
        first_token = tree.children[0]
        if self.is_target_language_name_set:
            self.errors.append( "Duplicated target language name defined in your grammar on: %s" % ( first_token.pretty() ) )

        self.is_target_language_name_set = True
        return self.__default__(tree.data, tree.children, tree.meta)

    def master_scope_name_statement(self, tree):
        first_token = tree.children[0]
        if self.is_master_scope_name_set:
            self.errors.append( "Duplicated master scope name defined in your grammar on: %s" % ( first_token.pretty() ) )

        self.is_master_scope_name_set = True
        return self.__default__(tree.data, tree.children, tree.meta)

    def include_statement(self, tree):
        first_token = tree.children[0]
        include_name = str(first_token)

        self.required_includes[include_name] = first_token
        return self.__default__(tree.data, tree.children, tree.meta)

    def match_statement(self, tree):
        first_token = tree.children[0]
        include_name = str(first_token)

        try:
            re.compile(include_name)

        except re.error as error:
            self.errors.append( "Invalid regular expression `%s` on match statement:\n   %s" % ( include_name, error) )

        return self.__default__(tree.data, tree.children, tree.meta)

    def _check_for_main_rules(self):
        """
            Look for missing required main rules on the grammar preamble statement.
        """
        if not self.is_master_scope_name_set:
            self.errors.append( "Missing master scope name in your grammar preamble." )

        if not self.is_target_language_name_set:
            self.errors.append( "Missing target language name in your grammar preamble." )

    def _check_for_unused_includes(self):
        """
            Look for missing required main rules on the grammar preamble statement.
        """
        for include_name, include_token in self.defined_includes.items():
            if include_name not in self.required_includes:
                self.warnings.append( "Unused include `%s` defined in your grammar on: %s" % ( include_name, include_token.pretty() ) )

    def _check_for_missing_includes(self):
        """
            Look for missing required includes by the `include` statement.
        """
        for include_name, include_token in self.required_includes.items():
            if include_name not in self.defined_includes:
                self.errors.append( "Missing include `%s` defined in your grammar on: %s" % ( include_name, include_token.pretty() ) )

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
            return self.__default__(tree.data, tree.children, tree.meta)
        else:
            return f(tree)
