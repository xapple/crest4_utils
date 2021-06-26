#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.

A script to convert the old format crest databases to the new
format used in `crest4`.
"""

# Imports #
import inspect
from autopaths import Path
from fasta import FASTA

# Get the current directory of this python script #
this_file = Path((inspect.stack()[0])[1])
this_dir  = this_file.directory

###############################################################################
class OldDatabase:
    """
    Represents an old formatted CREST database.
    """

    @property
    def base_dir(self):
        # The directory of the old database #
        return this_dir + '../../databases_orig/' + self.short_name + '/'

    @property
    def new_dir(self):
        # The destination directory for the new database #
        return this_dir + '../../databases/' + self.short_name + '/'

    #--------------------------- Old file names ------------------------------#
    @property
    def orig_tre(self):
        return self.base_dir + self.short_name + '.tre'

    @property
    def orig_map(self):
        return self.base_dir + self.short_name + '.map'

    @property
    def orig_fasta(self):
        return FASTA(self.base_dir + self.short_name + '.fasta')

    #--------------------------- New file names ------------------------------#
    @property
    def new_tre(self):
        return self.new_dir + self.short_name + '.tre'

    @property
    def new_map(self):
        return self.new_dir + self.short_name + '.map'

    @property
    def new_names(self):
        return self.new_dir + self.short_name + '.names'

    @property
    def new_fasta(self):
        return FASTA(self.new_dir + self.short_name + '.fasta')

    #------------------------------- Conversion ------------------------------#
    def convert_map(self):
        # How to convert the lines #
        def process(lines):
            result = []
            for line in lines:
                num, name, minus, frac = line.strip().split('\t')
                if ',' in name: raise Exception("Got a comma in the name.")
                if frac != '-1': continue
                result.append((num, name))
            result.sort(key=lambda elem: int(elem[0]))
            for item in result:
                yield ','.join(item) + '\n'
        # Convert the old to new #
        with open(self.orig_map, 'rt') as old, \
             open(self.new_map, 'wt') as new:
            new.writelines(process(old))
        return self.new_map

    def convert_names(self):
        # How to convert the lines #
        def process(lines):
            result = []
            for line in lines:
                num, name, minus, frac = line.strip().split('\t')
                if frac == '-1': break
                result.append((num, name, frac))
            result.sort(key=lambda elem: int(elem[0]))
            for item in result:
                yield ','.join(item) + '\n'
        # Convert the old to new #
        with open(self.orig_map, 'rt') as old, \
             open(self.new_names, 'wt') as new:
            new.writelines(process(old))
        return self.new_names

    def convert_fasta(self):
        # Remove duplicate entries #
        self.new_fasta.remove_duplicates()
        # Back transcribe #
        self.new_fasta.convert_U_to_T()

    def convert(self):
        self.convert_map()
        self.convert_names()
        self.convert_fasta()

###############################################################################
class SilvaMod128(OldDatabase):
    """
    Represents the old silvamod database.
    """

    # The real name #
    short_name = 'silvamod128'

#-----------------------------------------------------------------------------#
class SilvaMod138(OldDatabase):
    """
    Represents the new silvamod database.
    """

    # The real name #
    short_name = 'silvamod138'

###############################################################################
# As our databases should only be converted on disk once, we have singletons #
silvamod128 = SilvaMod128()
silvamod138 = SilvaMod138()

# How to use these objects #
if __name__ == '__main__':
    silvamod138.convert()
