
import re
import pushdown

from pushdown import Tree

from debug_tools import getLogger
from debug_tools.utilities import get_representation

log = getLogger(__name__)


class Backend(pushdown.Interpreter):

    def __init__(self, tree, program, theme):
        super().__init__()
        self.tree = tree
        self.program = program
        self.theme = theme

        self.visit(tree)
        log( 1, "Tree: \n%s", tree.pretty(debug=0) )

    def target_language_name_statement(self, tree):
        target_language_name = tree.children[0]

        self.target_language_name = target_language_name
        log( 1, "target_language_name: %s", self.target_language_name )

    def master_scope_name_statement(self, tree):
        master_scope_name = tree.children[0]

        self.master_scope_name = master_scope_name
        log( 1, "master_scope_name: %s", self.master_scope_name )

    def match_statement(self, tree):
        match = tree.children[0]
        self.match = match

        log( 1, "match: %s", self.match )
        self.visit_children(tree)

    def scope_name(self, tree):
        scope_name = tree.children[0]

        self.scope_name = scope_name
        log( 1, "scope_name: %s", self.scope_name )

    def generated_html(self):
        log( 1, "..." )


