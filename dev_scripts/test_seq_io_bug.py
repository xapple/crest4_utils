#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to test a bug in biopython's SearchIO parsing
"""

# Modules #
from io import StringIO
from Bio import SearchIO

###############################################################################
# First case #
no_repeats = """
Query1\tHit1\t99.8\t1310\t2\t0\t1\t1497\t1\t1310\t-1\t0
Query1\tHit2\t99.6\t1393\t5\t0\t1\t1497\t1\t1393\t-1\t0
Query1\tHit3\t99.1\t1497\t10\t1\t1\t1497\t1\t1499\t-1\t0
Query2\tHit1\t99.8\t1310\t2\t0\t1\t1497\t1\t1310\t-1\t0
Query2\tHit2\t99.6\t1393\t5\t0\t1\t1497\t1\t1393\t-1\t0
Query2\tHit3\t99.1\t1497\t10\t1\t1\t1497\t1\t1499\t-1\t0
"""

# Second case #
direct_repeats = """
Query1\tHit1\t99.8\t1310\t2\t0\t1\t1497\t1\t1310\t-1\t0
Query1\tHit2\t99.6\t1393\t5\t0\t1\t1497\t1\t1393\t-1\t0
Query1\tHit2\t99.1\t1497\t10\t1\t1\t1497\t1\t1499\t-1\t0
Query2\tHit1\t99.8\t1310\t2\t0\t1\t1497\t1\t1310\t-1\t0
Query2\tHit3\t99.6\t1393\t5\t0\t1\t1497\t1\t1393\t-1\t0
Query2\tHit3\t99.1\t1497\t10\t1\t1\t1497\t1\t1499\t-1\t0
"""

# Second case #
later_repeats = """
Query1\tHit1\t99.8\t1310\t2\t0\t1\t1497\t1\t1310\t-1\t0
Query1\tHit2\t99.6\t1393\t5\t0\t1\t1497\t1\t1393\t-1\t0
Query1\tHit1\t99.1\t1497\t10\t1\t1\t1497\t1\t1499\t-1\t0
Query2\tHit3\t99.8\t1310\t2\t0\t1\t1497\t1\t1310\t-1\t0
Query2\tHit1\t99.6\t1393\t5\t0\t1\t1497\t1\t1393\t-1\t0
Query2\tHit3\t99.1\t1497\t10\t1\t1\t1497\t1\t1499\t-1\t0
"""

###############################################################################
handle = StringIO(no_repeats.lstrip())
handle.seek(0)
parser = SearchIO.parse(handle, 'blast-tab')
result = list(parser)

handle = StringIO(direct_repeats.lstrip())
handle.seek(0)
parser = SearchIO.parse(handle, 'blast-tab')
result = list(parser)

handle = StringIO(later_repeats.lstrip())
handle.seek(0)
parser = SearchIO.parse(handle, 'blast-tab')
result = list(parser)

###############################################################################
# With comments activated #
handle = StringIO(no_repeats)
parser = SearchIO.parse(handle, 'blast-tab', comments=True)
result = list(parser)