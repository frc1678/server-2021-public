#!/usr/bin/env python3
# Copyright (c) 2019 FRC Team 1678: Citrus Circuits
"""Changes font size of tablets for app consistency."""
from data_transfer import adb_communicator
import utils


FILE_PATH = utils.create_file_path('data/tablets')
utils.run_command(f'rm -R {FILE_PATH}', True)
utils.run_command(f'mkdir {FILE_PATH}', True)
adb_communicator.adb_font_size_enforcer()
