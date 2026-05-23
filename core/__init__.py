# __init__.py
"""
The Alcyoneus DB (The Alcy)
Exceeding the average reasonable limits of databases in the OSINT database field

A comprehensive OSINT database for tracking usernames, emails, phone numbers,
and digital footprints across 500+ platforms with anti-false-positive validation.

Author: ZK-Phantom Team
Version: 1.0.0
License: Educational Purpose Only
"""

__version__ = "1.0.0"
__author__ = "TheZ4th"
__description__ = "The Alcyoneus DB - Exceeding OSINT database limits"

from .database import AlcyoneusDB
from .hunter import UsernameHunter
from .validator import AntiFalsePositiveValidator
from .exporter import DataExporter
from .grapher import GrapherSystem
__all__ = [
    'AlcyoneusDB',
    'UsernameHunter',
    'AntiFalsePositiveValidator',
    'DataExporter',
    'GrapherSystem'
]
