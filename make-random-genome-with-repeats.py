#! /usr/bin/env python
import random

N_REPEATS=10

random.seed(1)                  # make reproducible

x = ["A"] + ["G"] + ["C"] + ["T"]
x = x*100000

y = ["A"] + ["G"] + ["C"] + ["T"]
y = y*1000

random.shuffle(x)
random.shuffle(y)

x = "".join(x)
y = "".join(y)

z = []
chunksize = len(x) / N_REPEATS
for i in range(0, len(x), chunksize):
    z.append(x[i:i+chunksize])
    z.append(y)

print '>repgenome\n%s\n' % "".join(z)
