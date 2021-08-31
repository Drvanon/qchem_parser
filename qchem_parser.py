#! python3
from lark import Lark
from transformers import CleanNamespaceToken, CleanNamespaceTree, Base, Parse
from pathlib import Path
from pprint import pformat
from manipulators import correct_tddft_transition_number
import click
import sys

parser = Lark.open(
        Path(__file__).parents[0] / "grammar" / "parser.lark",
        import_paths=[Path(__file__).parents[0] / 'grammar'])

def parse(string, fix_occupied=True):
    tree = parser.parse(string)
    transformer = CleanNamespaceToken() * Base() * CleanNamespaceTree() * Parse()
    resulting_tree = transformer.transform(tree) 
    result = resulting_tree.children
    if fix_occupied:
        correct_tddft_transition_number(result)
    return result

def pretty(string):
    tree = parser.parse(string)
    click.echo(tree.pretty())

def debug_f(string):
    tree = parser.parse(string)
    transformer = CleanNamespaceToken() * Base() #* CleanNamespaceTree()
    tree = transformer.transform(tree) 
    click.echo(tree.pretty())
    

@click.command()
@click.argument("inputfile", type=click.File('r'))
@click.option("-p", "--pretty-print", is_flag=True)
@click.option("-d", "--debug", is_flag=True)
@click.option("-n", "--no-fix_occupied", is_flag=True)
def main(inputfile, pretty_print, debug, no_fix_occupied):
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
    parsed = parse(fstr, fix_occupied=not no_fix_occupied)
    # This should become json.dumps when the output is no longer a Tree instance.
    click.echo(pformat(parsed))


if __name__ == "__main__":
    main()
