#!/usr/bin/env python3
"""
Data Sources Package
Contains all data source implementations for the Movember AI Rules System.
"""

# Import all data sources for easy access
from .aihw_source import AIHWDataSource
from .pcf_source import PCFDataSource
from .tcf_source import TCFDataSource
from .pubmed_source import PubMedDataSource
from .grants_gov_source import GrantsGovDataSource
from .nhmrc_source import NHMRCDataSource
from .beyond_blue_source import BeyondBlueDataSource
from .arc_source import ARCDataSource

__all__ = [
    'AIHWDataSource',
    'PCFDataSource', 
    'TCFDataSource',
    'PubMedDataSource',
    'GrantsGovDataSource',
    'NHMRCDataSource',
    'BeyondBlueDataSource',
    'ARCDataSource'
] 