from lark import Tree
from lark.visitors import Transformer, Discard, v_args
from pprint import pprint
from warnings import warn

class CleanNamespaceToken(Transformer):
    def __default_token__(self, token):
        token.type = token.type.split("__", 1)[-1]
        return token

class CleanNamespaceTree(Transformer):
    def __default__(self, data, children, meta):
        data = data.split("__", 1)[-1]
        return Tree(data, children, meta)

class Base(Transformer):
    FLOAT = float
    SIGNED_FLOAT = float
    INT = int 

    def excited_states__multiplicity(self, children):
        return Tree('excited_states__multiplicity', [children[0].lower()])

    def excited_states__method(self, children):
        return children[0].value
        
    def excited_states(self, children):        
        if type(children[0]) != str:
            warn(f"Type of a children[0] 'typeof({children[0]})' is not string, can not use it as a 'data' for a Tree().")
        return Tree(children[0], children[1:])

class Parse(Transformer):
    def __default__(self, data, children, meta):
        if len(children) == 0:
            return Tree(data, children, meta)
        elif isinstance(children[0], Tree):
            if len(set([child.data for child in children])) == 1:
                return Tree(data, [child.children for child in children], meta)
            return Tree(data, { child.data: child.children for child in children }, meta)
        elif len(children) == 1:
            return Tree(data, children[0], meta)
        else:
            return Tree(data, children, meta)

