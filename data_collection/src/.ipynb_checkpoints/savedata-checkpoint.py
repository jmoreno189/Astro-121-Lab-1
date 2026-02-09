"""
Author: Joseph Moreno
Description: Python module designed to save data to the ..\measurements folder. Files and directories are labeled with appropriate metadata unique to the collected data.
"""

import os

def save_file(data=None, metadata=None):
    assert data is not None, "Save attempt failed: missing data."
    assert metadata is not None
    
