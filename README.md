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
