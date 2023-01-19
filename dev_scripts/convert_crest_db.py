#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.

A script to convert the old format crest databases to the new
format used in `crest4`.
"""

# Imports #
import os, inspect, sh
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

    @property
    def new_tar_gz(self):
        return self.new_dir.directory + self.short_name + '.tar.gz'

    #------------------------------- Conversion ------------------------------#
    def convert_map(self):
        # How to convert the lines #
        def process_map(lines):
            # Initialize #
            result = []
            for line in lines:
                # Parse the line #
                num, name, minus, frac = line.strip().split('\t')
                # Check if we are still in the names at the top of the file #
                if frac != '-1': continue
                # Remove commas #
                if ',' in name:
                    print("Removed a comma from '%s'" % name)
                    name = name.replace(',', '')
                # Add this entry #
                result.append((num, name))
            # Sort all entries #
            result.sort(key=lambda elem: int(elem[0]))
            # Return entries one by one #
            for item in result:
                yield ','.join(item) + '\n'
        # Convert the old to new #
        with open(self.orig_map, 'rt') as old, \
             open(self.new_map, 'wt') as new:
            new.writelines(process_map(old))
        # Return #
        return self.new_map

    def convert_names(self):
        # How to convert the lines #
        def process_names(lines):
            # Initialize #
            result = []
            for line in lines:
                # Parse the line #
                num, name, minus, frac = line.strip().split('\t')
                # Check if we have reached the maps at the bottom of the file #
                if frac == '-1': break
                # Remove commas #
                if ',' in name:
                    print("Removed a comma from '%s'" % name)
                    name = name.replace(',', '')
                # Add this entry #
                result.append((num, name, frac))
            # Sort all entries #
            result.sort(key=lambda elem: int(elem[0]))
            # Return entries one by one #
            for item in result:
                yield ','.join(item) + '\n'
        # Convert the old to new #
        with open(self.orig_map, 'rt') as old, \
             open(self.new_names, 'wt') as new:
            new.writelines(process_names(old))
        # Return #
        return self.new_names

    def convert_fasta(self):
        # If the FASTA is not present, copy it from the original #
        if not self.new_fasta:
            print("\nDuplicated the FASTA file to '%s'" % self.new_fasta.with_tilda)
            self.orig_fasta.copy(self.new_fasta)
        # Remove duplicate entries #
        self.new_fasta.remove_duplicates()
        # Back transcribe #
        self.new_fasta.convert_U_to_T()

    def convert(self):
        # Message #
        msg = "\nConverting database '%s' to '%s'"
        print(msg % (self.base_dir.with_tilda, self.new_dir.with_tilda))
        # Create a directory if it doesn't exist #
        self.new_dir.create_if_not_exists()
        # Call methods #
        print("\nConverting file '%s'" %  self.orig_map.with_tilda)
        self.convert_map()
        self.convert_names()
        print("\nConverting file '%s'" %  self.orig_fasta.with_tilda)
        self.convert_fasta()
        # Copy the tree file #
        self.orig_tre.copy(self.new_tre)

    @property
    def db(self):
        from crest4 import databases
        db = getattr(databases, self.short_name)
        return db

    def check(self):
        # Check that the parsing of the resulting files works #
        print("\nChecking file '%s'" % self.new_map)
        # Map file #
        print("Number of entries in map file: ", len(self.db.acc_to_node))
        # Names file #
        print("Number of entries in names file: ", len(self.db.node_to_name))
        # Tree file #
        print("Number of nodes in tree file: ", len(self.db.tree))

    def compress(self):
        # Prepare to compress the directory #
        print("Compressing the directory at '%s'" % self.new_dir.with_tilda)
        env_vars = os.environ.copy()
        env_vars['COPYFILE_DISABLE'] = '1'
        options = ["--no-mac-metadata", "--exclude", ".DS_Store",
                   "--options", "gzip:compression-level=9", "-zcvf"]
        # Compress the directory #
        os.chdir(self.new_dir.directory)
        sh.tar(*options, self.new_tar_gz, self.short_name,
               _env=env_vars, _fg=True)

    def upload(self):
        # Message #
        print("Upload the file at '%s'" % self.new_tar_gz.with_tilda)
        # Get the AWS S3 resource #
        import boto3
        s3 = boto3.resource('s3')
        # Get the bucket #
        bucket = s3.Bucket('crest4')
        # Upload #
        return bucket.upload_file(self.new_tar_gz, self.new_tar_gz.name)

    def make_public(self):
        """
        A method to make the newly uploaded object in the AWS S3 bucket
        readable by anyone. #TODO
        """
        pass

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

#-----------------------------------------------------------------------------#
class Bold(OldDatabase):
    """
    Represents the new bold database.
    """

    # The real name #
    short_name = 'bold'

#-----------------------------------------------------------------------------#
class Midori248(OldDatabase):
    """
    Represents the new midori database.
    """

    # The real name #
    short_name = 'midori248'

#-----------------------------------------------------------------------------#
class SilvaMod138Pr2(OldDatabase):
    """
    Represents the new silvamod138pr2 v2 database.
    """

    # The real name #
    short_name = 'silvamod138pr2'

###############################################################################
# As our databases should only be converted on disk once, we have singletons #
silvamod128    = SilvaMod128()
silvamod138    = SilvaMod138()
bold           = Bold()
midori248      = Midori248()
silvamod138pr2 = SilvaMod138Pr2()

# Example of how to use these objects #
if __name__ == '__main__':
    #silvamod138pr2.convert()
    silvamod138pr2.check()
    #silvamod138pr2.compress()
    #silvamod138pr2.upload()
    #silvamod138pr2.make_public()