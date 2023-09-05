#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.

A script to test tree libraries.

Other options:
* treelib (almost no functionality)
* anytree
* NetworkX

Results:

    ---------- treeswift ----------
    Total elapsed time: 0:00:00.131250
    ---------- ete3 ----------
    Total elapsed time: 0:00:00.571757
    ---------- dendropy ----------
    Total elapsed time: 0:00:00.962512
    ---------- biopython ----------
    Total elapsed time: 0:00:00.048447
"""

# Imports #
import inspect
from plumbing.timer import Timer
from autopaths import Path

# Get the current directory of this python script #
this_file = Path((inspect.stack()[0])[1])
this_dir  = this_file.directory

# Path to database #
db_path = this_dir.directory + 'databases/silvamod128/silvamod128.tre'

###############################################################################
################################### trsw ######################################
print("-"*10 + ' treeswift ' + "-"*10)
with Timer(True):
    from treeswift import read_tree_newick
    tree = read_tree_newick(db_path)


###############################################################################
################################### ete3 ######################################
print("-"*10 + ' ete3 ' + "-"*10)
with Timer(True):
    import ete3
    tree_ete3 = ete3.Tree(db_path)


###############################################################################
################################### ddpy ######################################
print("-"*10 + ' dendropy ' + "-"*10)
with Timer(True):
    import dendropy
    tree_ddpy = dendropy.Tree.get(path=db_path, schema='newick')


###############################################################################
################################### biop ######################################
print("-"*10 + ' biopython ' + "-"*10)
with Timer(True):
    from Bio import Phylo
    tree_biop = Phylo.parse(db_path, 'newick')


