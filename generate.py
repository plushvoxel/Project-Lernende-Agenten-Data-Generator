#!/usr/bin/env python3

from io import BytesIO
import subprocess
from threading import Thread
from tempfile import NamedTemporaryFile

SAMP_RATE = int(0.5e6)

am = subprocess.Popen(['./grc/am_noisy.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

## PWM generator function
# Args:
#   period:     number of samples per perio
#   duty_cycle: float from 0 to 1
def pwm(period, duty_cycle):
    while True:
        for i in range(int(duty_cycle*period)):
            yield 1
        for i in range(int((1-duty_cycle)*period)):
            yield 0

def producer():
    for period in range(SAMP_RATE//10, SAMP_RATE+1, SAMP_RATE//10):
        for duty_cycle_percent in range(0, 101, 10):
            arr = [x for _, x in zip(range(SAMP_RATE), pwm(period, duty_cycle_percent/100))]
            am.stdin.write(bytes(arr))
    # crude hack
    try:
        am.stdin.write(b'\x00'*SAMP_RATE*2)
    except:
        pass

prod = Thread(target=producer)
prod.start()
for period in range(SAMP_RATE//10, SAMP_RATE+1, SAMP_RATE//10):
    for duty_cycle_percent in range(0, 101, 10):
        with NamedTemporaryFile(mode='w+b', suffix='.iq', prefix='am_', dir='./iq/', delete=False) as file:
            # file.open()
            file.write(am.stdout.read(SAMP_RATE*8))

am.kill()
