#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.

A script to check if taxonomic names are repeated in different levels of the
tree when ingesting a NDS file. For example, if "Eukaryota" appears as both
a genus and a species name across the dataset.
"""

# Built-in modules #
import csv, argparse, gzip
from collections import defaultdict
from functools import cached_property

###############################################################################
class AccessionTSV:
    """
    Represents a TSV file with three columns. Example line:
    OQ071217    Main genome/Eukaryota/.../Antalis agilis    Antalis agilis
    """

    # ------------------------------ Methods -------------------------------- #
    def __init__(self, path):
        """Here we record the full path of the input file."""
        self.tsv_path = path

    @cached_property
    def taxa_levels(self):
        """
        Store names and the levels (ranks) they appear at,
        along with accessions.
        """
        return defaultdict(lambda: {'ranks': set(), 'accessions': {}})

    def __iter__(self):
        """Here we create a CSV reader object on the input file."""
        # Check if file is gzipped by reading the magic number #
        with open(self.tsv_path, 'rb') as f:
            magic_number = f.read(2)
        # Open with gzip if magic number matches  #
        if magic_number.startswith(b'\x1f\x8b'):
            file_obj = gzip.open(self.tsv_path, 'rt')
        else:
            file_obj = open(self.tsv_path)
        # Return the reader #
        return csv.reader(file_obj, delimiter='\t')

    def __call__(self):
        """
        Iterate all lines, record each taxonomic name and its level(s).
        Report all the names found at multiple distinct levels.
        """
        # Iterate over rows #
        for row in self:
            # Parse the row #
            acc, path, full_name = row
            # Split the path into a list #
            path = path.split('/')
            # Join numerical segments back with their preceding segments #
            fixed_path = []
            for i, segment in enumerate(path):
                if segment.isdigit() and i > 0:
                    fixed_path[-1] = fixed_path[-1] + '/' + segment
                else:
                    fixed_path.append(segment)
            # Make a list of tuples with names and ranks associated #
            with_ranks = list(zip(fixed_path, range(1, len(fixed_path)+1)))
            # Record each name and its rank #
            for name, rank in with_ranks:
                self.taxa_levels[name]['ranks'].add(rank)
                # Only store the first accession we see for each rank
                if rank not in self.taxa_levels[name]['accessions']:
                    self.taxa_levels[name]['accessions'][rank] = acc
        # Report any names that appear at multiple ranks #
        print("\nNames appearing at multiple ranks:")
        print("--------------------------------")
        for name, data in sorted(self.taxa_levels.items()):
            if len(data['ranks']) > 1:
                print(f"\n{name}: appears at ranks {sorted(data['ranks'])}")
                print("Example accessions:")
                for rank in sorted(data['ranks']):
                    print(f"  - {data['accessions'][rank]} (rank {rank})")

###############################################################################
if __name__ == '__main__':
    # Make an arugment parser #
    desc = ("Check a 3-column TSV (accession, lineage, name) for taxonomic ",
            "names appearing at multiple distinct levels")
    parser = argparse.ArgumentParser(description=desc)
    # Add our single argument #
    parser.add_argument(
        "tsv_file",
        metavar = "TSV_FILE",
        type    = str,
        help    = "Path to the input TSV file (can be gzipped)."
    )
    # Parse arguments from command line #
    args = parser.parse_args()
    # Create an instance of the processor #
    checker = AccessionTSV(args.tsv_file)
    # Run the check #
    checker()