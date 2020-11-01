#!/bin/py

# The data in Excel is at a frequency of 30 minutes. I need it at an interval
# of 5 minutes. This calls for a resampling. The function in this file does
# it.

def resample(T):
    T1 = [[n] * 6 for n in T]
    T2 = [n for sublist in T1 for n in sublist]

    return T2

