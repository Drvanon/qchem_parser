from lark import Lark
from transformers import Base, Parse
from pathlib import Path
from pprint import pformat
import click
import sys

parser = Lark.open("grammar/parser.lark", rel_to=Path(__file__).parents[0] / 'grammar')

def parse(string):
    tree = parser.parse(string)
    transformer = Base() * Parse()
    result = transformer.transform(tree) 
    return result

def pretty(string):
    tree = parser.parse(string)
    click.echo(tree.pretty())

@click.command()
@click.argument("inputfile", type=click.File('r'))
@click.option("-p", "--pretty-print", is_flag=True)
def main(inputfile, pretty_print):
    fstr = inputfile.read()
    inputfile.close()
    if pretty_print:
        pretty(fstr)
        sys.exit()

    # Transformation returns the 'start' Tree instance, which contains the 
    # dict in it's children property.
    parsed = parse(fstr).children
    # This should become json.dumps when the output is no longer a Tree instance.
    click.echo(pformat(parsed))


if __name__ == "__main__":
    main()
