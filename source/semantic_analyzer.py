
import lark
from lark import Tree, LarkError, Token

from debug_tools import getLogger
log = getLogger(__name__)


class SemanticErrors(LarkError):
    def __init__(self, exceptions):
        counter = [0]

        def increment(exception):
            counter[0] += 1
            return str(exception)

        self.messages = "\n1. " + ( "\n%s. " % counter[0] ).join( increment(exception) for exception in exceptions )

    def __str__(self):
        return self.messages


class TreeTransformer(lark.Transformer):
    """
        Transforms the Derivation Tree nodes into meaningful string representations,
        allowing simple recursive parsing parsing and conversion to Abstract Syntax Tree.
    """

    ## Saves all the semantic errors errors detected so far
    errors = []

    ## Can only be one scope called `contexts`
    has_called_language_construct_rules = False

    def language_syntax(self, tree):
        """
            This is the grammar start symbol and will be called by last with all
            partial subtrees the start symbol derivates.

            This is a great place to check whether global grammar properties
            where set.
        """

        if not self.has_called_language_construct_rules:
            self.errors.append("You must to define the `contexts` block in your grammar!")

        if self.errors:
            raise SemanticErrors(self.errors)

        return self.__default__(tree.data, tree.children, tree.meta)

    def language_construct_rules(self, tree):
        self.has_called_language_construct_rules = True
        return self.__default__(tree.data, tree.children, tree.meta)

    def miscellaneous_language_rules(self, tree):
        first_token = tree.children[0]
        assert tree.data == 'miscellaneous_language_rules', "Just documenting what the data attribute has."
        assert isinstance( first_token, Token ), "The first children must be a Token, while the second is a subtree."

        if str(first_token) == 'contexts':
            self.errors.append("Extra `contexts` rule defined in your grammar on: %s" % first_token.pretty())

        return self.__default__(tree.data, tree.children, tree.meta)

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