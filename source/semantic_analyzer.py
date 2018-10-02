
import lark
from lark import Tree, LarkError, Token

from debug_tools import getLogger
log = getLogger(__name__)


class SemanticErrors(LarkError):
    def __init__(self, exceptions):
        # https://stackoverflow.com/questions/16625068/combine-lists-by-joining-strings-with-matching-index-values
        messages = map( lambda a, b: "%s. %s" % (a, b), range( 1, len(exceptions) + 1 ), exceptions )
        self.messages = "\n".join( message for message in messages )

    def __str__(self):
        return self.messages


class TreeTransformer(lark.Transformer):
    """
        Transforms the Derivation Tree nodes into meaningful string representations,
        allowing simple recursive parsing parsing and conversion to Abstract Syntax Tree.
    """

    def __init__(self):
        ## Saves all the semantic errors errors detected so far
        self.errors = []

        ## Can only be one scope called `contexts`
        self.has_called_language_construct_rules = False

        ## A list of miscellaneous_language_rules include contexts defined for duplication checking
        self.defined_includes = []

        ## A list of required includes to check for missing includes
        self.required_includes = []

    def language_syntax(self, tree):
        """
            This is the grammar start symbol and will be called by last with all
            partial subtrees the start symbol derivates.

            This is a great place to check whether global grammar properties
            where set.
        """

        if not self.has_called_language_construct_rules:
            self.errors.append("You must to define the `contexts` block in your grammar!")

        self._check_for_missing_includes()

        if self.errors:
            raise SemanticErrors(self.errors)

        return self.__default__(tree.data, tree.children, tree.meta)

    def language_construct_rules(self, tree):
        self.has_called_language_construct_rules = True
        return self.__default__(tree.data, tree.children, tree.meta)

    def miscellaneous_language_rules(self, tree):
        first_token = tree.children[0]
        include_name = str(first_token)
        assert tree.data == 'miscellaneous_language_rules', "Just documenting what the data attribute has."
        assert isinstance( first_token, Token ), "The first children must be a Token, while the second is a subtree."

        if include_name == 'contexts':
            self.errors.append("Extra `contexts` rule defined in your grammar on: %s" % first_token.pretty())

        if include_name in self.defined_includes:
            self.errors.append("Duplicated include `%s` defined in your grammar on: %s" % ( include_name, first_token.pretty()))

        self.defined_includes.append(include_name)
        return self.__default__(tree.data, tree.children, tree.meta)

    def include_statement(self, tree):
        first_token = tree.children[0]
        include_name = str(first_token)

        self.required_includes.append( (include_name, first_token) )
        return self.__default__(tree.data, tree.children, tree.meta)

    def _check_for_missing_includes(self):
        """
            Look for missing required includes by the `include` statement.
        """
        for include_name, include_token in self.required_includes:
            if include_name not in self.defined_includes:
                self.errors.append("Missing include `%s` defined in your grammar on: %s" % ( include_name, include_token.pretty() ) )

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
