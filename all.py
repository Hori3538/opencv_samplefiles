#!/usr/bin/env python
# Run all

import importlib
import os
import re

re = re.compile('\d_[\dn]+.py')
files = list([f for f in os.listdir() if re.match(f)])
files = list([os.path.splitext(f)[0] for f in files])
files.sort()

for ff in files:
    print('Running {}'.format(ff))
    importlib.import_module(ff)
