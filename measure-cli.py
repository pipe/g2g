# MIT License
#
# Copyright (c) 2024 |pipe|
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import time

ADC.setup()
GPIO.setup("P2_6", GPIO.OUT)
GPIO.output("P2_6", GPIO.LOW)
start = int(round(time.time() * 1000))
value = 0.0
maxv = 0.0
minv = 1.0
for x in range (0,5000):
    v= ADC.read("P1_19")
    value = value+ v
    if (v > maxv):
        maxv = v
    if (v < minv):
        minv = v

GPIO.output("P2_6", GPIO.HIGH)

for x in range (0,5000):
    v = ADC.read("P1_19")
    value = value+ v
    if (v > maxv):
        maxv = v
    if (v < minv):
        minv = v

dur = int(round(time.time() * 1000)) - start
average = value/10000.0

rv = int(round((maxv - minv) * 100.0))
print ("average",average," in ",dur," range is ",rv," % ")
td = 0
if (rv > 25):
    for n in range (0,50):
        GPIO.output("P2_6", GPIO.LOW)
        start = int(round(time.time() * 1000)) 
        c=0
        value = ADC.read("P1_19")
        while  value > average:
            value = ADC.read("P1_19")
        dur = int(round(time.time() * 1000)) - start
        GPIO.output("P2_6", GPIO.HIGH)
        td = td + dur
        time.sleep(1)

print ("mean rtt is ",td/50)
