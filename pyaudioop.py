# -*- coding: utf-8 -*-
"""
Mock pyaudioop module for Python 3.13+ compatibility.
This provides stubs for the functions that pydub expects.
"""

import warnings

def _not_implemented(*args, **kwargs):
    """Placeholder function that warns about missing functionality."""
    warnings.warn("pyaudioop functionality not available in Python 3.13+. This is a compatibility stub.", 
                  RuntimeWarning, stacklevel=2)
    return None

# Common pyaudioop functions that pydub might use
add = _not_implemented
adpcm2lin = _not_implemented
adpcm32lin = _not_implemented
adpcm42lin = _not_implemented
alaw2lin = _not_implemented
avg = _not_implemented
avgpp = _not_implemented
bias = _not_implemented
cross = _not_implemented
findfactor = _not_implemented
findfit = _not_implemented
findmax = _not_implemented
getsample = _not_implemented
lin2adpcm = _not_implemented
lin2adpcm3 = _not_implemented
lin2adpcm4 = _not_implemented
lin2alaw = _not_implemented
lin2lin = _not_implemented
lin2ulaw = _not_implemented
max = _not_implemented
maxpp = _not_implemented
minmax = _not_implemented
mul = _not_implemented
ratecv = _not_implemented
reverse = _not_implemented
rms = _not_implemented
tomono = _not_implemented
tostereo = _not_implemented
ulaw2lin = _not_implemented
