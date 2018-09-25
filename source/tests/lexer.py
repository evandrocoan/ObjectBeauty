# The file was automatically generated by Lark v0.6.4
#
#
#   Lark Stand-alone Generator Tool
# ----------------------------------
# Generates a stand-alone LALR(1) parser with a standard lexer
#
# Git:    https://github.com/erezsh/lark
# Author: Erez Shinan (erezshin@gmail.com)
#
#
#    >>> LICENSE
#
#    This tool and its generated code use a separate license from Lark.
#
#    It is licensed under GPLv2 or above.
#
#    If you wish to purchase a commercial license for this tool and its
#    generated code, contact me via email.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    See <http://www.gnu.org/licenses/>.
#
#

class LarkError(Exception):
    pass

class GrammarError(LarkError):
    pass

class ParseError(LarkError):
    pass

class LexError(LarkError):
    pass

class UnexpectedInput(LarkError):
    pos_in_stream = None

    def get_context(self, text, span=40):
        pos = self.pos_in_stream
        start = max(pos - span, 0)
        end = pos + span
        before = text[start:pos].rsplit('\n', 1)[-1]
        after = text[pos:end].split('\n', 1)[0]
        return before + after + '\n' + ' ' * len(before) + '^\n'

    def match_examples(self, parse_fn, examples):
        """ Given a parser instance and a dictionary mapping some label with
            some malformed syntax examples, it'll return the label for the
            example that bests matches the current error.
        """
        assert self.state is not None, "Not supported for this exception"

        candidate = None
        for label, example in examples.items():
            assert not isinstance(example, STRING_TYPE)

            for malformed in example:
                try:
                    parse_fn(malformed)
                except UnexpectedInput as ut:
                    if ut.state == self.state:
                        try:
                            if ut.token == self.token:  # Try exact match first
                                return label
                        except AttributeError:
                            pass
                        if not candidate:
                            candidate = label

        return candidate


class UnexpectedCharacters(LexError, UnexpectedInput):
    def __init__(self, seq, lex_pos, line, column, allowed=None, considered_tokens=None, state=None):
        message = "No terminal defined for '%s' at line %d col %d" % (seq[lex_pos], line, column)

        self.line = line
        self.column = column
        self.allowed = allowed
        self.considered_tokens = considered_tokens
        self.pos_in_stream = lex_pos
        self.state = state

        message += '\n\n' + self.get_context(seq)
        if allowed:
            message += '\nExpecting: %s\n' % allowed

        super(UnexpectedCharacters, self).__init__(message)



class UnexpectedToken(ParseError, UnexpectedInput):
    def __init__(self, token, expected, considered_rules=None, state=None):
        self.token = token
        self.expected = expected     # XXX str shouldn't necessary
        self.line = getattr(token, 'line', '?')
        self.column = getattr(token, 'column', '?')
        self.considered_rules = considered_rules
        self.state = state
        self.pos_in_stream = getattr(token, 'pos_in_stream', None)

        message = ("Unexpected token %r at line %s, column %s.\n"
                   "Expected one of: \n\t* %s\n"
                   % (token, self.line, self.column, '\n\t* '.join(self.expected)))

        super(UnexpectedToken, self).__init__(message)


try:
    STRING_TYPE = basestring
except NameError:   # Python 3
    STRING_TYPE = str


import types
from functools import wraps, partial
from contextlib import contextmanager

Str = type(u'')

def smart_decorator(f, create_decorator):
    if isinstance(f, types.FunctionType):
        return wraps(f)(create_decorator(f, True))

    elif isinstance(f, (type, types.BuiltinFunctionType)):
        return wraps(f)(create_decorator(f, False))

    elif isinstance(f, types.MethodType):
        return wraps(f)(create_decorator(f.__func__, True))

    elif isinstance(f, partial):
        # wraps does not work for partials in 2.7: https://bugs.python.org/issue3445
        return create_decorator(f.__func__, True)

    else:
        return create_decorator(f.__func__.__call__, True)




class Meta:
    pass

class Tree(object):
    def __init__(self, data, children, meta=None):
        self.data = data
        self.children = children
        self._meta = meta

    @property
    def meta(self):
        if self._meta is None:
            self._meta = Meta()
        return self._meta

    def __repr__(self):
        return 'Tree(%s, %s)' % (self.data, self.children)

    def _pretty_label(self):
        return self.data

    def _pretty(self, level, indent_str):
        if len(self.children) == 1 and not isinstance(self.children[0], Tree):
            return [ indent_str*level, self._pretty_label(), '\t', '%s' % (self.children[0],), '\n']

        l = [ indent_str*level, self._pretty_label(), '\n' ]
        for n in self.children:
            if isinstance(n, Tree):
                l += n._pretty(level+1, indent_str)
            else:
                l += [ indent_str*(level+1), '%s' % (n,), '\n' ]

        return l

    def pretty(self, indent_str='  '):
        return ''.join(self._pretty(0, indent_str))
    def __eq__(self, other):
        try:
            return self.data == other.data and self.children == other.children
        except AttributeError:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.data, tuple(self.children)))

from inspect import getmembers, getmro

class Discard(Exception):
    pass

# Transformers

class Transformer:
    """Visits the tree recursively, starting with the leaves and finally the root (bottom-up)

    Calls its methods (provided by user via inheritance) according to tree.data
    The returned value replaces the old one in the structure.

    Can be used to implement map or reduce.
    """

    def _call_userfunc(self, tree, new_children=None):
        # Assumes tree is already transformed
        children = new_children if new_children is not None else tree.children
        try:
            f = getattr(self, tree.data)
        except AttributeError:
            return self.__default__(tree.data, children, tree.meta)
        else:
            if getattr(f, 'meta', False):
                return f(children, tree.meta)
            elif getattr(f, 'inline', False):
                return f(*children)
            elif getattr(f, 'whole_tree', False):
                if new_children is not None:
                    raise NotImplementedError("Doesn't work with the base Transformer class")
                return f(tree)
            else:
                return f(children)

    def _transform_children(self, children):
        for c in children:
            try:
                yield self._transform_tree(c) if isinstance(c, Tree) else c
            except Discard:
                pass

    def _transform_tree(self, tree):
        children = list(self._transform_children(tree.children))
        return self._call_userfunc(tree, children)

    def transform(self, tree):
        return self._transform_tree(tree)

    def __mul__(self, other):
        return TransformerChain(self, other)

    def __default__(self, data, children, meta):
        "Default operation on tree (for override)"
        return Tree(data, children, meta)

    @classmethod
    def _apply_decorator(cls, decorator, **kwargs):
        mro = getmro(cls)
        assert mro[0] is cls
        libmembers = {name for _cls in mro[1:] for name, _ in getmembers(_cls)}
        for name, value in getmembers(cls):
            if name.startswith('_') or name in libmembers:
                continue

            setattr(cls, name, decorator(value, **kwargs))
        return cls


class InlineTransformer(Transformer):   # XXX Deprecated
    def _call_userfunc(self, tree, new_children=None):
        # Assumes tree is already transformed
        children = new_children if new_children is not None else tree.children
        try:
            f = getattr(self, tree.data)
        except AttributeError:
            return self.__default__(tree.data, children, tree.meta)
        else:
            return f(*children)


class TransformerChain(object):
    def __init__(self, *transformers):
        self.transformers = transformers

    def transform(self, tree):
        for t in self.transformers:
            tree = t.transform(tree)
        return tree

    def __mul__(self, other):
        return TransformerChain(*self.transformers + (other,))


class Transformer_InPlace(Transformer):
    "Non-recursive. Changes the tree in-place instead of returning new instances"
    def _transform_tree(self, tree):           # Cancel recursion
        return self._call_userfunc(tree)

    def transform(self, tree):
        for subtree in tree.iter_subtrees():
            subtree.children = list(self._transform_children(subtree.children))

        return self._transform_tree(tree)


class Transformer_InPlaceRecursive(Transformer):
    "Recursive. Changes the tree in-place instead of returning new instances"
    def _transform_tree(self, tree):
        tree.children = list(self._transform_children(tree.children))
        return self._call_userfunc(tree)



# Visitors

class VisitorBase:
    def _call_userfunc(self, tree):
        return getattr(self, tree.data, self.__default__)(tree)

    def __default__(self, tree):
        "Default operation on tree (for override)"
        return tree


class Visitor(VisitorBase):
    """Bottom-up visitor, non-recursive

    Visits the tree, starting with the leaves and finally the root (bottom-up)
    Calls its methods (provided by user via inheritance) according to tree.data
    """


    def visit(self, tree):
        for subtree in tree.iter_subtrees():
            self._call_userfunc(subtree)
        return tree

class Visitor_Recursive(VisitorBase):
    """Bottom-up visitor, recursive

    Visits the tree, starting with the leaves and finally the root (bottom-up)
    Calls its methods (provided by user via inheritance) according to tree.data
    """

    def visit(self, tree):
        for child in tree.children:
            if isinstance(child, Tree):
                self.visit(child)

        f = getattr(self, tree.data, self.__default__)
        f(tree)
        return tree



def visit_children_decor(func):
    "See Interpreter"
    @wraps(func)
    def inner(cls, tree):
        values = cls.visit_children(tree)
        return func(cls, values)
    return inner


class Interpreter:
    """Top-down visitor, recursive

    Visits the tree, starting with the root and finally the leaves (top-down)
    Calls its methods (provided by user via inheritance) according to tree.data

    Unlike Transformer and Visitor, the Interpreter doesn't automatically visit its sub-branches.
    The user has to explicitly call visit_children, or use the @visit_children_decor
    """
    def visit(self, tree):
        return getattr(self, tree.data)(tree)

    def visit_children(self, tree):
        return [self.visit(child) if isinstance(child, Tree) else child
                for child in tree.children]

    def __getattr__(self, name):
        return self.__default__

    def __default__(self, tree):
        return self.visit_children(tree)




# Decorators

def _apply_decorator(obj, decorator, **kwargs):
    try:
        _apply = obj._apply_decorator
    except AttributeError:
        return decorator(obj, **kwargs)
    else:
        return _apply(decorator, **kwargs)



def _inline_args__func(func):
    @wraps(func)
    def create_decorator(_f, with_self):
        if with_self:
            def f(self, children):
                return _f(self, *children)
        else:
            def f(self, children):
                return _f(*children)
        return f

    return smart_decorator(func, create_decorator)


def inline_args(obj):   # XXX Deprecated
    return _apply_decorator(obj, _inline_args__func)



def _visitor_args_func_dec(func, inline=False, meta=False, whole_tree=False):
    assert [whole_tree, meta, inline].count(True) <= 1
    def create_decorator(_f, with_self):
        if with_self:
            def f(self, *args, **kwargs):
                return _f(self, *args, **kwargs)
        else:
            def f(self, *args, **kwargs):
                return _f(*args, **kwargs)
        return f

    f = smart_decorator(func, create_decorator)
    f.inline = inline
    f.meta = meta
    f.whole_tree = whole_tree
    return f

def v_args(inline=False, meta=False, tree=False):
    "A convenience decorator factory, for modifying the behavior of user-supplied visitor methods"
    if [tree, meta, inline].count(True) > 1:
        raise ValueError("Visitor functions can either accept tree, or meta, or be inlined. These cannot be combined.")
    def _visitor_args_dec(obj):
        return _apply_decorator(obj, _visitor_args_func_dec, inline=inline, meta=meta, whole_tree=tree)
    return _visitor_args_dec



class Indenter:
    def __init__(self):
        self.paren_level = 0
        self.indent_level = [0]

    def handle_NL(self, token):
        if self.paren_level > 0:
            return

        yield token

        indent_str = token.rsplit('\n', 1)[1] # Tabs and spaces
        indent = indent_str.count(' ') + indent_str.count('\t') * self.tab_len

        if indent > self.indent_level[-1]:
            self.indent_level.append(indent)
            yield Token.new_borrow_pos(self.INDENT_type, indent_str, token)
        else:
            while indent < self.indent_level[-1]:
                self.indent_level.pop()
                yield Token.new_borrow_pos(self.DEDENT_type, indent_str, token)

            assert indent == self.indent_level[-1], '%s != %s' % (indent, self.indent_level[-1])

    def process(self, stream):
        for token in stream:
            if token.type == self.NL_type:
                for t in self.handle_NL(token):
                    yield t
            else:
                yield token

            if token.type in self.OPEN_PAREN_types:
                self.paren_level += 1
            elif token.type in self.CLOSE_PAREN_types:
                self.paren_level -= 1
                assert self.paren_level >= 0

        while len(self.indent_level) > 1:
            self.indent_level.pop()
            yield Token(self.DEDENT_type, '')

        assert self.indent_level == [0], self.indent_level

    # XXX Hack for ContextualLexer. Maybe there's a more elegant solution?
    @property
    def always_accept(self):
        return (self.NL_type,)


class Token(Str):
    __slots__ = ('type', 'pos_in_stream', 'value', 'line', 'column', 'end_line', 'end_column')

    def __new__(cls, type_, value, pos_in_stream=None, line=None, column=None):
        self = super(Token, cls).__new__(cls, value)
        self.type = type_
        self.pos_in_stream = pos_in_stream
        self.value = value
        self.line = line
        self.column = column
        self.end_line = None
        self.end_column = None
        return self

    @classmethod
    def new_borrow_pos(cls, type_, value, borrow_t):
        return cls(type_, value, borrow_t.pos_in_stream, line=borrow_t.line, column=borrow_t.column)

    def __reduce__(self):
        return (self.__class__, (self.type, self.value, self.pos_in_stream, self.line, self.column, ))

    def __repr__(self):
        return 'Token(%s, %r)' % (self.type, self.value)

    def __deepcopy__(self, memo):
        return Token(self.type, self.value, self.pos_in_stream, self.line, self.column)

    def __eq__(self, other):
        if isinstance(other, Token) and self.type != other.type:
            return False

        return Str.__eq__(self, other)

    __hash__ = Str.__hash__


class LineCounter:
    def __init__(self):
        self.newline_char = '\n'
        self.char_pos = 0
        self.line = 1
        self.column = 1
        self.line_start_pos = 0

    def feed(self, token, test_newline=True):
        """Consume a token and calculate the new line & column.

        As an optional optimization, set test_newline=False is token doesn't contain a newline.
        """
        if test_newline:
            newlines = token.count(self.newline_char)
            if newlines:
                self.line += newlines
                self.line_start_pos = self.char_pos + token.rindex(self.newline_char) + 1

        self.char_pos += len(token)
        self.column = self.char_pos - self.line_start_pos + 1

class _Lex:
    "Built to serve both Lexer and ContextualLexer"
    def __init__(self, lexer, state=None):
        self.lexer = lexer
        self.state = state

    def lex(self, stream, newline_types, ignore_types):
        newline_types = list(newline_types)
        ignore_types = list(ignore_types)
        line_ctr = LineCounter()

        t = None
        while True:
            lexer = self.lexer
            for mre, type_from_index in lexer.mres:
                m = mre.match(stream, line_ctr.char_pos)
                if m:
                    value = m.group(0)
                    type_ = type_from_index[m.lastindex]
                    if type_ not in ignore_types:
                        t = Token(type_, value, line_ctr.char_pos, line_ctr.line, line_ctr.column)
                        if t.type in lexer.callback:
                            t = lexer.callback[t.type](t)
                        yield t
                    else:
                        if type_ in lexer.callback:
                            t = Token(type_, value, line_ctr.char_pos, line_ctr.line, line_ctr.column)
                            lexer.callback[type_](t)

                    line_ctr.feed(value, type_ in newline_types)
                    if t:
                        t.end_line = line_ctr.line
                        t.end_column = line_ctr.column

                    break
            else:
                if line_ctr.char_pos < len(stream):
                    raise UnexpectedCharacters(stream, line_ctr.char_pos, line_ctr.line, line_ctr.column, state=self.state)
                break

        if t:
            t.end_line = line_ctr.line
            t.end_column = line_ctr.column

class UnlessCallback:
    def __init__(self, mres):
        self.mres = mres

    def __call__(self, t):
        for mre, type_from_index in self.mres:
            m = mre.match(t.value)
            if m:
                t.type = type_from_index[m.lastindex]
                break
        return t


from functools import partial, wraps


class ExpandSingleChild:
    def __init__(self, node_builder):
        self.node_builder = node_builder

    def __call__(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return self.node_builder(children)


class PropagatePositions:
    def __init__(self, node_builder):
        self.node_builder = node_builder

    def __call__(self, children):
        res = self.node_builder(children)
        res.meta.empty = True

        if children and isinstance(res, Tree):
            for c in children:
                if isinstance(c, Tree) and c.children and not c.meta.empty:
                    res.meta.line = c.meta.line
                    res.meta.column = c.meta.column
                    res.meta.start_pos = c.meta.start_pos
                    res.meta.empty = False
                    break
                elif isinstance(c, Token):
                    res.meta.line = c.line
                    res.meta.column = c.column
                    res.meta.start_pos = c.pos_in_stream
                    res.meta.empty = False
                    break

            for c in reversed(children):
                if isinstance(c, Tree) and c.children and not c.meta.empty:
                    res.meta.end_line = c.meta.end_line
                    res.meta.end_column = c.meta.end_column
                    res.meta.end_pos = c.meta.end_pos
                    res.meta.empty = False
                    break
                elif isinstance(c, Token):
                    res.meta.end_line = c.end_line
                    res.meta.end_column = c.end_column
                    res.meta.end_pos = c.pos_in_stream + len(c.value)
                    res.meta.empty = False
                    break

        return res


class ChildFilter:
    def __init__(self, to_include, node_builder):
        self.node_builder = node_builder
        self.to_include = to_include

    def __call__(self, children):
        filtered = []
        for i, to_expand in self.to_include:
            if to_expand:
                filtered += children[i].children
            else:
                filtered.append(children[i])

        return self.node_builder(filtered)

class ChildFilterLALR(ChildFilter):
    "Optimized childfilter for LALR (assumes no duplication in parse tree, so it's safe to change it)"

    def __call__(self, children):
        filtered = []
        for i, to_expand in self.to_include:
            if to_expand:
                if filtered:
                    filtered += children[i].children
                else:   # Optimize for left-recursion
                    filtered = children[i].children
            else:
                filtered.append(children[i])

        return self.node_builder(filtered)

def _should_expand(sym):
    return not sym.is_term and sym.name.startswith('_')

def maybe_create_child_filter(expansion, keep_all_tokens, ambiguous):
    to_include = [(i, _should_expand(sym)) for i, sym in enumerate(expansion)
                  if keep_all_tokens or not (sym.is_term and sym.filter_out)]

    if len(to_include) < len(expansion) or any(to_expand for i, to_expand in to_include):
        return partial(ChildFilter if ambiguous else ChildFilterLALR, to_include)


class Callback(object):
    pass


def ptb_inline_args(func):
    @wraps(func)
    def f(children):
        return func(*children)
    return f



class ParseTreeBuilder:
    def __init__(self, rules, tree_class, propagate_positions=False, keep_all_tokens=False, ambiguous=False):
        self.tree_class = tree_class
        self.propagate_positions = propagate_positions
        self.always_keep_all_tokens = keep_all_tokens
        self.ambiguous = ambiguous

        self.rule_builders = list(self._init_builders(rules))

        self.user_aliases = {}

    def _init_builders(self, rules):
        for rule in rules:
            options = rule.options
            keep_all_tokens = self.always_keep_all_tokens or (options.keep_all_tokens if options else False)
            expand_single_child = options.expand1 if options else False

            wrapper_chain = filter(None, [
                (expand_single_child and not rule.alias) and ExpandSingleChild,
                maybe_create_child_filter(rule.expansion, keep_all_tokens, self.ambiguous),
                self.propagate_positions and PropagatePositions,
            ])

            yield rule, wrapper_chain


    def create_callback(self, transformer=None):
        callback = Callback()

        i = 0
        for rule, wrapper_chain in self.rule_builders:
            internal_callback_name = '_cb%d_%s' % (i, rule.origin)
            i += 1

            user_callback_name = rule.alias or rule.origin.name
            try:
                f = getattr(transformer, user_callback_name)
                assert not getattr(f, 'meta', False), "Meta args not supported for internal transformer"
                # XXX InlineTransformer is deprecated!
                if getattr(f, 'inline', False) or isinstance(transformer, InlineTransformer):
                    f = ptb_inline_args(f)
            except AttributeError:
                f = partial(self.tree_class, user_callback_name)

            self.user_aliases[rule] = rule.alias
            rule.alias = internal_callback_name

            for w in wrapper_chain:
                f = w(f)

            if hasattr(callback, internal_callback_name):
                raise GrammarError("Rule '%s' already exists" % (rule,))
            setattr(callback, internal_callback_name, f)

        return callback



class _Parser:
    def __init__(self, parse_table, callbacks):
        self.states = parse_table.states
        self.start_state = parse_table.start_state
        self.end_state = parse_table.end_state
        self.callbacks = callbacks

    def parse(self, seq, set_state=None):
        token = None
        stream = iter(seq)
        states = self.states

        state_stack = [self.start_state]
        value_stack = []

        if set_state: set_state(self.start_state)

        def get_action(key):
            state = state_stack[-1]
            try:
                return states[state][key]
            except KeyError:
                expected = [s for s in states[state].keys() if s.isupper()]
                raise UnexpectedToken(token, expected, state=state)  # TODO filter out rules from expected

        def reduce(rule):
            size = len(rule.expansion)
            if size:
                s = value_stack[-size:]
                del state_stack[-size:]
                del value_stack[-size:]
            else:
                s = []

            value = self.callbacks[rule](s)

            _action, new_state = get_action(rule.origin.name)
            assert _action is Shift
            state_stack.append(new_state)
            value_stack.append(value)

        # Main LALR-parser loop
        # print(''); index = -1
        for token in stream:
            # index += 1; x = token; print(repr(f"[@{index},{x.pos_in_stream}:{x.pos_in_stream+len(x.value)-1}='{x.value}'<{x.type}>,{x.line}:{x.column}]"))
            while True:
                action, arg = get_action(token.type)
                assert arg != self.end_state

                if action is Shift:
                    state_stack.append(arg)
                    value_stack.append(token)
                    if set_state: set_state(arg)
                    break # next token
                else:
                    reduce(arg)

        token = Token.new_borrow_pos('<EOF>', token, token) if token else Token('<EOF>', '', 0, 1, 1)
        while True:
            _action, arg = get_action('$END')
            if _action is Shift:
                assert arg == self.end_state
                val ,= value_stack
                return val
            else:
                reduce(arg)


class Symbol(object):
    is_term = NotImplemented

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        assert isinstance(other, Symbol), other
        return self.is_term == other.is_term and self.name == other.name

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.name)

    fullrepr = property(__repr__)

class Terminal(Symbol):
    is_term = True

    def __init__(self, name, filter_out=False):
        self.name = name
        self.filter_out = filter_out

    @property
    def fullrepr(self):
        return '%s(%r, %r)' % (type(self).__name__, self.name, self.filter_out)


class NonTerminal(Symbol):
    is_term = False

class Rule(object):
    """
        origin : a symbol
        expansion : a list of symbols
    """
    def __init__(self, origin, expansion, alias=None, options=None):
        self.origin = origin
        self.expansion = expansion
        self.alias = alias
        self.options = options

    def __str__(self):
        return '<%s : %s>' % (self.origin, ' '.join(map(str,self.expansion)))

    def __repr__(self):
        return 'Rule(%r, %r, %r, %r)' % (self.origin, self.expansion, self.alias, self.options)


class RuleOptions:
    def __init__(self, keep_all_tokens=False, expand1=False, priority=None):
        self.keep_all_tokens = keep_all_tokens
        self.expand1 = expand1
        self.priority = priority

    def __repr__(self):
        return 'RuleOptions(%r, %r, %r)' % (
            self.keep_all_tokens,
            self.expand1,
            self.priority,
        )

Shift = 0
Reduce = 1
import re
class LexerRegexps: pass
NEWLINE_TYPES = []
IGNORE_TYPES = []
LEXERS = {}
MRES = (
[('(?P<A>A)', {1: 'A'})]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[0] = (lexer_regexps)
MRES = (
[('(?P<B>B)', {1: 'B'})]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[1] = (lexer_regexps)
MRES = (
[]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[2] = (lexer_regexps)
MRES = (
[('(?P<AB>AB)', {1: 'AB'})]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[3] = (lexer_regexps)
MRES = (
[('(?P<AB>AB)', {1: 'AB'})]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[4] = (lexer_regexps)
MRES = (
[]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[5] = (lexer_regexps)
MRES = (
[]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[6] = (lexer_regexps)
MRES = (
[]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[7] = (lexer_regexps)
class ContextualLexer:
    def __init__(self):
        self.lexers = LEXERS
        self.set_parser_state(None)
    def set_parser_state(self, state):
        self.parser_state = state
    def lex(self, stream):
        newline_types = NEWLINE_TYPES
        ignore_types = IGNORE_TYPES
        lexers = LEXERS
        l = _Lex(lexers[self.parser_state], self.parser_state)
        for x in l.lex(stream, newline_types, ignore_types):
            yield x
            l.lexer = lexers[self.parser_state]
            l.state = self.parser_state
CON_LEXER = ContextualLexer()
def lex(stream):
    return CON_LEXER.lex(stream)
RULES = {
  0: Rule(NonTerminal('start'), [NonTerminal('a'), NonTerminal('b')], None, RuleOptions(False, False, None)),
  1: Rule(NonTerminal('a'), [Terminal('A', True), Terminal('B', True)], None, RuleOptions(False, False, None)),
  2: Rule(NonTerminal('b'), [Terminal('AB', True)], None, RuleOptions(False, False, None)),
}
parse_tree_builder = ParseTreeBuilder(RULES.values(), Tree)
class ParseTable: pass
parse_table = ParseTable()
STATES = {
  0: {0: (0, 1), 1: (0, 2), 2: (0, 3)},
  1: {3: (0, 4)},
  2: {4: (0, 5)},
  3: {5: (0, 6), 6: (0, 7)},
  4: {6: (1, 1)},
  5: {},
  6: {4: (1, 0)},
  7: {4: (1, 2)},
}
TOKEN_TYPES = (
{0: 'A', 1: 'start', 2: 'a', 3: 'B', 4: '$END', 5: 'b', 6: 'AB'}
)
parse_table.states = {s: {TOKEN_TYPES[t]: (a, RULES[x] if a is Reduce else x) for t, (a, x) in acts.items()}
                      for s, acts in STATES.items()}
parse_table.start_state = 0
parse_table.end_state = 5
class Lark_StandAlone:
  def __init__(self, transformer=None, postlex=None):
     callback = parse_tree_builder.create_callback(transformer=transformer)
     callbacks = {rule: getattr(callback, rule.alias or rule.origin, None) for rule in RULES.values()}
     self.parser = _Parser(parse_table, callbacks)
     self.postlex = postlex
  def parse(self, stream):
     tokens = lex(stream)
     sps = CON_LEXER.set_parser_state
     if self.postlex: tokens = self.postlex.process(tokens)
     return self.parser.parse(tokens, sps)