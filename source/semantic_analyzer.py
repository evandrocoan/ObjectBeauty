
import lark
from lark import Tree

class TreeTransformer(lark.Transformer):
    """
        Transforms the AST (Abstract Syntax Tree) nodes into meaningful string representations,
        allowing simple recursive parsing parsing of the AST tree.
    """

    def start_symbol(self, productions):
        """
            Converts the tree start symbol into a production ready to be used in the Chomsky Grammar.
        """
        log( 4, 'productions: %s', productions )
        return productions[0]

