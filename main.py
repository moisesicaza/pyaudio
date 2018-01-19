#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
req_version = (3, 0)
cur_version = sys.version_info

# Verify Python version.
if not sys.version_info[:2] >= req_version:
    print("A version of python >= 3.x is required.")

else:
    from pytomp3 import PyToMp3

    mp3 = PyToMp3()
    mp3.run()
