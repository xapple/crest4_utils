#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to generate the databases that Vsearch will use.
This process takes a FASTA as input and indexes it producing a file '.udb'
"""

# Built-in modules #
import sys

# Internal modules #
import crest4

# First party modules #
from seqsearch.search.vsearch import VSEARCHdb
from plumbing.scraping import download_from_url
from autopaths import Path

###############################################################################
# Where the original fasta file is located #
base_url  = "http://services.cbu.uib.no/supplementary/crest/fasta/"
file_name = "silvamod128.fasta.gz"

# The destination #
dest_dir = "~/repos/crest4/databases/silvamod128/"
dest_file = Path(dest_dir + file_name)

# Download #
download_from_url(base_url + file_name,
                  destination = dest_dir,
                  uncompress  = True,
                  user_agent  = "crest4 v" + crest4.__version__,
                  stream      = True,
                  progress    = True,
                  desc        = 'silvamod128')

# Remove the compressed file #
dest_file.remove()

# The resulting fasta #
fasta = VSEARCHdb(dest_file.prefix_path)

# Start the indexing #
fasta.makedb(verbose=True, stdout=sys.stdout)