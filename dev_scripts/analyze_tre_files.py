#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.

A script to print statistics about the tre and map files.
"""

# Imports #
import inspect
from autopaths import Path
import Bio.SeqIO.FastaIO
import ete3

# Get the current directory of this python script #
this_file = Path((inspect.stack()[0])[1])
this_dir  = this_file.directory

# Path to database #
map_path   = this_dir.directory + 'databases/silvamod128/silvamod128.map'
tre_path   = this_dir.directory + 'databases/silvamod128/silvamod128.tre'
names_path = this_dir.directory + 'databases/silvamod128/silvamod128.names'
fasta_path = this_dir.directory + 'databases/silvamod128/silvamod128.fasta'

###############################################################################
def parse_map_ids():
    with open(map_path, 'rt') as handle:
        for line in handle:
            yield line.split(',')[0].strip()

def parse_map_names():
    with open(map_path, 'rt') as handle:
        for line in handle:
            yield line.split(',')[1].strip()

def parse_tre_ids():
    tree = ete3.Tree(tre_path, format=8)
    for node in tree.traverse():
        yield node.name.strip()

def parse_names_ids():
    with open(names_path, 'rt') as handle:
        for line in handle:
            yield line.split(',')[0].strip()

def parse_fasta_ids():
    for seq in Bio.SeqIO.FastaIO.SimpleFastaParser(fasta_path):
        yield seq[0]

###############################################################################
def get_duplicates(seq):
  seen = set()
  seen_add = seen.add
  seen_twice = set( x for x in seq if x in seen or seen_add(x) )
  return seen_twice

###############################################################################
map_ids   = list(parse_map_ids())
map_names = list(parse_map_names())
tre_ids   = list(parse_tre_ids())
names_ids = list(parse_names_ids())
fasta_ids = list(parse_fasta_ids())

dup_map_ids   = get_duplicates(map_ids)
dup_map_names = get_duplicates(map_names)
dup_tre_ids   = get_duplicates(tre_ids)
dup_names_ids = get_duplicates(names_ids)
dup_fasta_ids = get_duplicates(fasta_ids)
