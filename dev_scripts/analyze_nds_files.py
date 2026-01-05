#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.

A script to print statistics about the NDS file exported by ARB.
"""

# Built-in modules #
import argparse

# Internal modules #
from make_new_crest_db import AccessionTSV

###############################################################################
class AnalysisNDS(AccessionTSV):
    """
    See script `make_new_crest_db.py`.
    """

    # ----------------------------- Properties ------------------------------ #
    @property
    def invalid_rows(self):
        """Return all the rows that have more than 3 columns."""
        for i, row in enumerate(self):
            # Check that the row has three columns #
            if len(row) != 3:
                yield row
    # ------------------------------- Methods ------------------------------- #
    def __call__(self):
        print(len(list(self.invalid_rows)))

###############################################################################
if __name__ == '__main__':
    # Create a shell parser #
    parser = argparse.ArgumentParser()

    # Ask for the main argument #
    help_msg = "The path to the NDS file to process."
    parser.add_argument("input_nds", help=help_msg, type=str)

    # Parse the shell arguments #
    args = parser.parse_args()
    nds_path = args.input_nds

    # Run it #
    nds = AnalysisNDS(nds_path)
    nds()

    # Show success #
    print("Success.")