#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

def notify(title, text):
    os.system("""
            osascript -e 'display notification "{}" with title "{}" sound name "Glass"'
            """.format(text, title))