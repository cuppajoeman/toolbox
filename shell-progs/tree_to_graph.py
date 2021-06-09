#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Convert a JSON to a graph."""

from __future__ import print_function
import json
import sys


def tree2graph(data, verbose=True):
    """
    Convert a JSON to a graph.

    Run `dot -Tpng -otree.png`

    Parameters
    ----------
    json_filepath : str
        Path to a JSON file
    out_dot_path : str
        Path where the output dot file will be stored

    Examples
    --------
    >>> s = {"Harry": [ "Bill", \
                       {"Jane": [{"Diane": ["Mary", "Mark"]}]}]}
    >>> tree2graph(s)
    [('Harry', 'Bill'), ('Harry', 'Jane'), ('Jane', 'Diane'), ('Diane', 'Mary'), ('Diane', 'Mark')]
    """
    # Extract tree edges from the dict
    edges = []

    def get_edges(treedict, parent=None):
        name = next(iter(treedict.keys()))
        if parent is not None:
            edges.append((parent, name))
        for item in treedict[name]:
            if isinstance(item, dict):
                get_edges(item, parent=name)
            elif isinstance(item, list):
                for el in item:
                    if isinstance(item, dict):
                        edges.append((parent, item.keys()[0]))
                        get_edges(item[item.keys()[0]])
                    else:
                        edges.append((parent, el))
            else:
                edges.append((name, item))
    get_edges(data)
    return edges


def main(json_filepath, out_dot_path, lr=False, verbose=True):
    """IO."""
    # Read JSON
    with open(json_filepath) as data_file:
        data = json.load(data_file)

    if verbose:
        # Convert back to JSON & print to stderr so we can verfiy that the tree
        # is correct.
        print(json.dumps(data, indent=4), file=sys.stderr)

    # Get edges
    edges = tree2graph(data, verbose)

    # Dump edge list in Graphviz DOT format
    with open(out_dot_path, 'w') as f:
        f.write('strict digraph tree {\n')
        if lr:
            f.write('rankdir="LR";\n')
        for row in edges:
            f.write('    "{0}" -> "{1}";\n'.format(*row))
        f.write('}\n')


def get_parser():
    """Get parser object for tree2graph.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input",
                        dest="json_filepath",
                        help="JSON FILE to read",
                        metavar="FILE",
                        required=True)
    parser.add_argument("-o", "--output",
                        dest="out_dot_path",
                        help="DOT FILE to write",
                        metavar="FILE",
                        required=True)
    return parser


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    args = get_parser().parse_args()
    main(args.json_filepath, args.out_dot_path, verbose=False)
