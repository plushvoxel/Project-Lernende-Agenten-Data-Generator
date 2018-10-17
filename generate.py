#!/usr/bin/env python3

from io import BytesIO
import subprocess
from threading import Thread
from tempfile import NamedTemporaryFile
import tarfile

SAMP_RATE = 2048
DUTY_CYCLE_STEP = 5
PERIOD_STEP = SAMP_RATE//100


modulations = ["fm", "am"]
domains = ["time", "frequency"]

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

def producer(dsp):
    for period in range(PERIOD_STEP, SAMP_RATE//2+1, PERIOD_STEP):
        for duty_cycle_percent in range(DUTY_CYCLE_STEP, 101, DUTY_CYCLE_STEP):
            arr = [x for _, x in zip(range(SAMP_RATE), pwm(period, duty_cycle_percent/100))]
            dsp.stdin.write(bytes(arr))
    # crude hack, do not attempt at home
    try:
        dsp.stdin.write(b'\x00'*SAMP_RATE*100)
    except:
        pass

def main():
    for domain in domains:
        tar = tarfile.open("{}.tar".format(domain), "w")
        for modulation in modulations:
            dsp = subprocess.Popen(["./grc/{}_noisy_{}.py".format(modulation, domain)], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            prod = Thread(target=producer, args=[dsp])
            prod.start()
            for period in range(PERIOD_STEP, SAMP_RATE//2+1, PERIOD_STEP):
                for duty_cycle_percent in range(DUTY_CYCLE_STEP, 101, DUTY_CYCLE_STEP):
                    buffer = dsp.stdout.read(SAMP_RATE*2*4)
                    info = tarfile.TarInfo("{}_{}_{}.iq".format(modulation, period, duty_cycle_percent))
                    info.size = len(buffer)
                    tar.addfile(info, BytesIO(buffer))
                    print("{} {}%".format(period, duty_cycle_percent))
            dsp.terminate()

if __name__ == "__main__":
    main()
