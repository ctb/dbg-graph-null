#! /usr/bin/env python
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--length', type=int, default=100000)
args = parser.parse_args()

LENGTH = args.length

random.seed(1)                  # make reproducible

x = ["A"] + ["G"] + ["C"] + ["T"]
x = x*LENGTH

random.shuffle(x)
x = x[:LENGTH]

print '>genome\n%s' % "".join(x)
