# Qchem parser - An extensible parser for QChem output

Qchem parsers parses the output of qchem jobs. It is written with flexibility,
extensibility and maintainability in mind.

## Installing
Ensure python3.7 or higher is installed on your system and run.

```bash
pip install click lark
```

## Usage
The qchem parser can be used as a standalone program to output the contents of
a .out file in json format to stdout, or the file stage can be skipped
altogether and be imported into a python script so that the contents can be
accessed directly. 

### Examples
Running the following in a bash terminal that has qchem_parser.py in the path,
will parse `H20.out` and store the parsed result in the `H20.json` file.
```bash
$ qchem_parser.py H20.out > H20.json
```

This little script goes through all files in the subfolder of the `outputfiles`
folder and if it is an output file, it will store the parsed output in the
dictionary, with the file path being the key.
```python
from qchem_parser import parse
from pathlib import Path

output_files = {}
for path in Path('outputfiles').glob("**/*"):
    if path.is_file() and path.suffix == ".out":
        with path.open('r') as f:
            output_files[path] = parse(f.read())
```

## Extending the program
The majority of the logic is used in qchem_parser is written in lark. What
follow is a simple introduction to lark, but a solid documentation of lark is
also [available](https://lark-parser.readthedocs.io/en/latest/).

In order to add a new section of output files to the parser it is recommend to
either find a spot in an already existing file or (if appropriate) add a new one
within the grammar folder. The first step is always to ensure that your new rule
is included in the grammar tree. The root can be found in `grammar/parser.lark`
as `start:`. You can add your rule as a new option at the rule (the pipe
character `|` distinguishes between options for a rule).

You won't start out with a rule that makes complete sense, often a sub rule will
be added that looks like
```
start: previous_rules
     | ...
     | your_rule

your_rule: HEADER _default+ FOOTER
```

The `_default` rule (which can be imported from `tokens`) matches any line,
which is useful when other information about the contents of the section you are
newly describing have not been (correctly) added. 

Notice that the underscore `_` at the start of `_default`? It is the reason why
it does not show up in the output of the program. Any rule prefixed with an
underscore is ignored and instead its children are directly added to the parent. 

Lark supports the `re` module of python, meaning that regex strings can be added
as part of rules. For example the string `/[-]{60}/` is a terminal that matches
60 consecutive `-` signs. This is often useful when declaring separators.

When describing a list like structure in the output files the approach
`qchem_parser` has used up to now has been to create a list rule, which
simply repeats either an element in the list or a `_default` rule.

```
your_section: (your_element|default)+
```

This allows for flexibility: if a new, un-described string is present within the
section, the parser will not break. 

The element itself than consists of a body that is often ignored. Here all the
contents of the individual elements are added in an optional fashion.
```
your_element: (_your_element_body|_default)+
_your_element_body: "String that occurs in the ouput file containing a number: " number
                  | "Other line with" characters "characters"
number: INT
characters: INT
```
This way the order or the precise constitution does not matter and the code
because more flexible. 

