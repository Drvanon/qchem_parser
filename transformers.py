from lark import Tree
from lark.visitors import Transformer, Discard, v_args
from pprint import pprint
from warnings import warn

class CleanNamespaceToken(Transformer):
    def __default_token__(self, token):
        token.type = token.type.rsplit("__", 1)[-1]
        return token

class CleanNamespaceTree(Transformer):
    def __default__(self, data, children, meta):
        data = data.rsplit("__", 1)[-1]
        return Tree(data, children, meta)

class Base(Transformer):
    FLOAT = float
    SIGNED_FLOAT = float
    INT = int 

    def __default_token__(self, token):
        return str(token)

    def tddft__excited_states__multiplicity(self, children):
        return Tree('tddft__excited_states__multiplicity', [children[0].lower()])

    def tddft__excited_states__method(self, children):
        return children[0]
        
    def tddft__excited_states(self, children):        
        if type(children[0]) != str:
            warn(f"Type of a children[0] 'typeof({children[0]})' is not string, can not use it as a 'data' for a Tree().")
        return Tree(children[0], children[1:])

class Parse(Transformer):
    def __default__(self, data, children, meta):
        # Assume that if a tree has one child it is an atom.
        if len(children) == 0:
            return Tree(data, children, meta)
        elif isinstance(children[0], Tree):
            # if the children are all of the same rule, assume a list structure
            if len(set([child.data for child in children if isinstance(child, Tree)])) == 1:
                return Tree(data, [child.children for child in children if isinstance(child, Tree)], meta)

            # if children have different rules than assume a dict structure
            new_children_dict = {}
            for child in children:
                if not isinstance(child, Tree): continue
                if child.data in new_children_dict:
                    warn(f"Overwriting key '{child.data}'")
                new_children_dict[child.data] = child.children
            return Tree(data, new_children_dict, meta)
        elif len(children) == 1:
            return Tree(data, children[0], meta)
        else:
            return Tree(data, children, meta)

