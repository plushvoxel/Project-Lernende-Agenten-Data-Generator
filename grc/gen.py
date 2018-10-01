#!/usr/bin/env python3

SAMP_RATE = int(0.5e6)

from sys import stdout

stdout.buffer.write(b'\x00'*SAMP_RATE)

