from lark import Tree
from lark.visitors import Transformer, Discard, v_args
from pprint import pprint

class Base(Transformer):
    FLOAT = float
    SIGNED_FLOAT = float
    INT = int 

    def multiplicity(self, children):
        return Tree('multiplicity', [children[0].lower()])

    def method(self, children):
        return children[0].value
        
    def excited_states(self, children):        
        return Tree(children[0], children[1:])

class Parse(Transformer):
    def __default__(self, data, children, meta):
        if isinstance(children[0], Tree):
            if len(set([child.data for child in children])) == 1:
                return Tree(data, [child.children for child in children])
            return Tree(data, { child.data: child.children for child in children })
        elif len(children) == 1:
            return Tree(data, children[0])
        else:
            return Tree(data, children)

