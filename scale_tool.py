#!/usr/bin/env python3
"""
Linnstrument Scale Tool - Main Command Line Interface
Automatically sets Linnstrument lights to reflect musical scales
"""

import argparse
import sys

from scales import get_scale_notes, get_available_scales, note_name_to_number, NOTE_NAMES
from linnstrument import Linnstrument
I dont' know whythwe lowe