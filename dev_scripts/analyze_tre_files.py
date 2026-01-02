#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.

A script to print statistics about the tre and map files.

To analyze all databases, you can run this:

    $ find ../databases -mindepth 1 -maxdepth 1 -type d -print0 | xargs -0 -n 1 ipython dev_scripts/analyze_tre_files.py
"""

# Imports #
import argparse
import inspect
from functools import cached_property
from autopaths import Path

# Get the current directory of this python script #
this_file = Path((inspect.stack()[0])[1])
this_dir  = this_file.directory

###############################################################################
class AnalyzeTree:

    default = 'silvamod138pr2'

    def __init__(self, db_dir):
        # Pick a default #
        default = this_dir + ('../../databases/%s/' % self.default)
        if db_dir is None: self.input_dir = Path(default.absolute_path)
        else: self.input_dir = Path(db_dir)
        # We need four files to be present #
        db_name = self.input_dir.name
        self.map_path   = self.input_dir + f'{db_name}.map'
        self.tre_path   = self.input_dir + f'{db_name}.tre'
        self.names_path = self.input_dir + f'{db_name}.names'
        self.fasta_path = self.input_dir + f'{db_name}.fasta'

    def __repr__(self):
        """A simple representation of this object to avoid memory addresses."""
        return "<%s object on '%s'>" % (self.__class__.__name__, self.input_dir)

    # ---------------------------- Properties ------------------------------- #
    @cached_property
    def tree3(self):
        """
        To use this property, you have to run max python 3.12.
        In python 3.13 and later, the `import cgi` module was removed from the
        standard library.
        """
        from ete3 import Tree as Tree3
        return Tree3(str(self.tre_path))

    @cached_property
    def tree4(self):
        """
        In ete4, unnamed internal nodes have node.name == None,
        while ete3 tends uses ''. So calling .strip() on ete4 can cause an
        exception to be raised.
        """
        from ete4 import Tree as Tree4
        return Tree4(str(self.tre_path))

    # ---------------------------- Node names ------------------------------- #
    def parse_tree3_ids(self):
        for node in self.tree3.traverse():
            yield node.name

    def parse_tree4_ids(self):
        for node in self.tree4.traverse():
            yield node.name

    def check_empty_names(self):
        """Return counts of unnamed nodes for ete3 and ete4."""
        # With ete 3 #
        tree3_empty = 0
        for name in self.parse_tree3_ids():
            if name is None or name == '':
                tree3_empty += 1
        # With ete 4 #
        tree4_empty = 0
        for name in self.parse_tree4_ids():
            if name is None or name == '':
                tree4_empty += 1
        # Return #
        return {'tree3': tree3_empty, 'tree4': tree4_empty}

    # ------------------------------ Methods -------------------------------- #
    def parse_map_ids(self):
        with open(self.map_path, 'rt') as handle:
            for line in handle:
                yield line.split(',')[0].strip()

    def parse_map_names(self):
        with open(self.map_path, 'rt') as handle:
            for line in handle:
                yield line.split(',')[1].strip()

    def parse_names_ids(self):
        with open(self.names_path, 'rt') as handle:
            for line in handle:
                yield line.split(',')[0].strip()

    def parse_fasta_ids(self):
        from Bio import SeqIO
        with open(self.fasta_path) as handle:
            for record in SeqIO.parse(handle, "fasta"):
                yield record.id

    def get_duplicates(self, seq):
        seen = set()
        add_to_seen = seen.add
        return set(x for x in seq if x in seen or add_to_seen(x))

    def __call__(self):
        map_ids   = list(self.parse_map_ids())
        map_names = list(self.parse_map_names())
        tre_ids   = list(self.parse_tree4_ids())
        names_ids = list(self.parse_names_ids())
        fasta_ids = list(self.parse_fasta_ids())

        dup_map_ids   = self.get_duplicates(map_ids)
        dup_map_names = self.get_duplicates(map_names)
        dup_tre_ids   = self.get_duplicates(tre_ids)
        dup_names_ids = self.get_duplicates(names_ids)
        dup_fasta_ids = self.get_duplicates(fasta_ids)

        print(f"dup_map_names : {dup_map_names}",  len(dup_map_names))
        print(f"dup_tre_ids   : {dup_tre_ids}",    len(dup_tre_ids))
        print(f"dup_names_ids : {dup_names_ids}",  len(dup_names_ids))
        print(f"dup_fasta_ids : {dup_fasta_ids}",  len(dup_fasta_ids))

###############################################################################
if __name__ == '__main__':
    # Make an argument parser #
    parser = argparse.ArgumentParser(
        description="Print statistics about a crest4 database."
    )
    # It has a single argument #
    parser.add_argument(
        "directory",
        nargs="?",
        default=None,
        help="Directory containing .map, .tre, .names, .fasta files",
    )
    # Run it #
    args = parser.parse_args()
    # Create an object #
    analysis = AnalyzeTree(args.directory)
    # Run some test functions #
    print(analysis)
    print(analysis.check_empty_names())