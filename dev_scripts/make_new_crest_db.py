#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.

A script to create new taxonomic databases formatted for use in `crest4`.

This script takes as input a "TSV" file. And generated the following output:

1) A `.tre` file
2) A `.map` file
3) A `.names` file.
"""

# Imports #
import os

###############################################################################
class AccessionTSV:
    """
    Represents a file with three columns:

    1) Accession.
    2) Path in the tree of life.
    3) Name of the taxa.

    Example:

        OQ071217    Main genome/Eukaryota/Amorphea/Metazoa/.../Antalis agilis    Antalis agilis
        OQ071218    Main genome/Eukaryota/Amorphea/Metazoa/.../Antalis agilis    Antalis agilis
        OQ071219    Main genome/Eukaryota/Amorphea/Metazoa/.../Antalis occidentalis  Antalis occidentalis
        OQ071220    Main genome/Eukaryota/Amorphea/Metazoa/.../Dacrydium vitreum     Dacrydium vitreum

    """

    @property
    def lorem(self):
        pass