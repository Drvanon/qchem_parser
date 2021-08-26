from lark import Lark
from transformers import CleanNamespaceToken, CleanNamespaceTree, Base, Parse
from pathlib import Path
from pprint import pformat
import click
import sys

parser = Lark.open("grammar/parser.lark", rel_to=Path(__file__).parents[0] / 'grammar')

def parse(string):
    tree = parser.parse(string)
    transformer = CleanNamespaceToken() * Base() * CleanNamespaceTree() * Parse()
    result = transformer.transform(tree) 
    return result

def pretty(string):
    tree = parser.parse(string)
    click.echo(tree.pretty())


from lark import Tree
def step_through_tree(tree, func):

    func(tree)
    for child in tree.children:
        if isinstance(child, Tree):
            step_through_tree(child, func)

def debug_f(string):
    tree = parser.parse(string)
    transformer = CleanNamespaceToken() * Base() * CleanNamespaceTree()
    tree = transformer.transform(tree) 
    step_through_tree(tree, lambda tree: print(f"{tree.data}"))
    click.echo(tree.pretty())
    

@click.command()
@click.argument("inputfile", type=click.File('r'))
@click.option("-p", "--pretty-print", is_flag=True)
@click.option("-d", "--debug", is_flag=True)
def main(inputfile, pretty_print, debug):
    fstr = inputfile.read()
    inputfile.close()
    if pretty_print:
        pretty(fstr)
        sys.exit()
    if debug:
        debug_f(fstr)
        sys.exit()

    # Transformation returns the 'start' Tree instance, which contains the 
    # dict in it's children property.
    parsed = parse(fstr).children
    # This should become json.dumps when the output is no longer a Tree instance.
    click.echo(pformat(parsed))


if __name__ == "__main__":
    main()
