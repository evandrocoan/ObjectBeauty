#! /usr/bin/env python
# -*- coding: utf-8 -*-

input_program = "void function() { }"

list_scopes = \
{
    0:  ["source.c", "storage.type.c"],
    4:  ["source.c", "function.definition.c", "function.definition.c"],
    13: ["source.c", "function.definition.c", "punctuation.open.paren.c"],
    14: ["source.c", "function.definition.c", "punctuation.close.paren.c"],
    16: ["source.c", "function.definition.c", "punctuation.open.braces.c"],
    16: ["source.c", "function.definition.c", "function.body.c"],
    18: ["source.c", "function.definition.c", "punctuation.close.braces.c"],
}

dict_scopes = {}
dict_scopes['source.c'] = (0,-1)
dict_scopes['function.definition.c'] = (0,-1)
dict_scopes['storage.type.c'] = (0,-1)

import pygtrie
trie = pygtrie.StringTrie()
trie['foo'] = 'Foo'
# trie['foo/bar'] = 'Bar'
trie['foo/bar/baz'] = 'Baz'

print('has_subtrie(foo):        ', trie.has_subtrie('foo'))
print('has_subtrie(foo/bar):    ', trie.has_subtrie('foo/bar'))
print('has_subtrie(foo/bar/baz):', trie.has_subtrie('foo/bar/baz'))
print('Trie.HAS_VALUE:                   ', trie.HAS_VALUE)
print('Trie.HAS_SUBTRIE:                 ', trie.HAS_SUBTRIE)
print('trie.HAS_VALUE | Trie.HAS_SUBTRIE:', trie.HAS_VALUE | trie.HAS_SUBTRIE)
print('has_node():            ', trie.has_node(''))
print('has_node(foo):         ', trie.has_node('foo'))
print('has_node(foo/bar):     ', trie.has_node('foo/bar'))
print('has_node(foo/bar/baz): ', trie.has_node('foo/bar/baz'))
print('has_node(foo/bar/baz/):', trie.has_node('foo/bar/baz/'))
print('has_key(foo):       ', trie.has_key('foo'))
print('has_key(foo/bar):   ', trie.has_key('foo/bar'))
print('has_key(foo/bar/baz):', trie.has_key('foo/bar/baz'))
print('longest_prefix:', trie.longest_prefix('foo'))
print('longest_prefix:', trie.longest_prefix('foo/bar'))
print('longest_prefix:', trie.longest_prefix('foo/bar/baz'))
print('shortest_prefix(foo):        ', trie.shortest_prefix('foo'))
print('shortest_prefix(foo/bar):    ', trie.shortest_prefix('foo/bar'))
print('shortest_prefix(foo/bar/baz):', trie.shortest_prefix('foo/bar/baz'))

def get_chunks(scope_name):
    pass

print( get_chunks( "function" ) )
print( get_chunks( "function punctuation" ) )
print( get_chunks( "function - punctuation" ) )

class Scope(object):
    def __init__(self, full_name):
        super().__init__()
        self.full_name = full_name



