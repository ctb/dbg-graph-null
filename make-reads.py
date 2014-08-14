#! /usr/bin/env python
import screed
import sys
import random
import fasta
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--error-rate', type=float, default=.01)
parser.add_argument('-r', '--read-length', type=int, default=100)
parser.add_argument('-C', '--coverage', type=int, default=50)
parser.add_argument('genome')
args = parser.parse_args()

random.seed(1)                  # make this reproducible, please.

COVERAGE=args.coverage
READLEN=args.read_length
ERROR_RATE=args.error_rate

record = iter(screed.open(args.genome)).next()
genome = record.sequence
len_genome = len(genome)

n_reads = int(len_genome*COVERAGE / float(READLEN))
reads_mut = 0
total_mut = 0

for i in range(n_reads):
    start = random.randint(0, len_genome - READLEN)
    read = genome[start:start + READLEN].upper()

    # reverse complement?
    if random.choice([0, 1]) == 0:
        read = fasta.rc(read)

    # error?
    was_mut = False
    for _ in range(READLEN):
        if ERROR_RATE > 0:
            while random.randint(1, int(1.0/ERROR_RATE)) == 1:
                pos = random.randint(1, READLEN) - 1
                read = read[:pos] + random.choice(['a', 'c', 'g', 't']) + read[pos+1:]
                was_mut = True
                total_mut += 1

    if was_mut:
        reads_mut += 1
    
    print '>read%d\n%s' % (i, read)

print >>sys.stderr, "%d of %d reads mutated; %d total mutations" % \
    (reads_mut, n_reads, total_mut)
