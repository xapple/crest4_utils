#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.

A script to download the old crest databases to disk.
"""

# Imports #
import inspect
import crest4
from autopaths import Path
from plumbing.scraping  import download_from_url

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
        # The destination directory #
        return this_dir + '../databases_orig/' + self.short_name + '/'

    def download_file(self, dest_dir, url):
        # Download #
        return download_from_url(url,
                                 destination = dest_dir,
                                 uncompress  = False,
                                 user_agent  = "crest4 v" + crest4.__version__,
                                 stream      = True,
                                 progress    = True,
                                 desc        = self.short_name)

    def download_tar(self):
        # Download #
        tar = self.download_file(self.base_dir, self.tar_url)
        # Uncompress #
        tar.untargz_to(self.base_dir)
        # Move files out one step and remove useless subdirectory #
        contents = self.base_dir + self.dir_name + '/'
        contents.unnest()
        # Remove tarball #
        tar.remove()

    def download_fasta(self):
        # Download #
        gz = self.download_file(self.base_dir, self.fasta_url)
        # Uncompress #
        if gz.endswith('.tar.gz'): gz.untargz_to()
        else:                      gz.ungzip_to()
        # Remove #
        gz.remove()

    def download(self):
        self.download_tar()
        self.download_fasta()

#-----------------------------------------------------------------------------#
class SilvaMod128(OldDatabase):
    """
    Represents the old silvamod database.
    """

    # The real name #
    short_name = 'silvamod128'

    # Addresses #
    tar_url = 'http://services.cbu.uib.no/supplementary/crest/silvamod128.tar.gz'
    fasta_url = 'http://services.cbu.uib.no/supplementary/crest/fasta/silvamod128.fasta.gz'

    # Others #
    dir_name = 'silvamod'

#-----------------------------------------------------------------------------#
class GreenGenes(OldDatabase):
    """
    Represents the old greengenes database.
    """

    # The real name #
    short_name = 'greengenes'

    # Addresses #
    tar_url = 'http://services.cbu.uib.no/supplementary/crest/greengenes.tar.gz'
    fasta_url = 'http://services.cbu.uib.no/supplementary/crest/fasta/greengenes.fasta.tar.gz'

    # Others #
    dir_name = 'greengenes'

    def download_fasta(self):
        raise NotImplementedError("The FASTA file is broken."
                                  "It is 404 HTML inside the tar.gz.")

###############################################################################
# As our databases should only be stored on disk once, we have singletons #
silvamod128 = SilvaMod128()
greengenes = GreenGenes()

# How to use these objects #
if __name__ == '__main__':
    # Download them #
    silvamod128.download()
    greengenes.download()
