#! /usr/bin/env python
import screed
import sys
import random
import fasta

random.seed(1)                  # make this reproducible, please.

COVERAGE=50
READLEN=100
ERROR_RATE=100
ARTIFACT_RATE=10000
ARTIFACT_SEQUENCE="CAAGGTGACTTAATGAAGCAACTGTAGGAAGA"

record = iter(screed.open(sys.argv[1])).next()
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
        if random.randint(1, ARTIFACT_RATE) == 1:
            read = read[:READLEN - len(ARTIFACT_SEQUENCE)] + ARTIFACT_SEQUENCE

        while random.randint(1, ERROR_RATE) == 1:

            pos = random.randint(1, READLEN) - 1
            read = read[:pos] + random.choice(['a', 'c', 'g', 't']) + read[pos+1:]
            was_mut = True
            total_mut += 1

    if was_mut:
        reads_mut += 1
    
    print '>read%d\n%s' % (i, read)

print >>sys.stderr, "%d of %d reads mutated; %d total mutations" % \
    (reads_mut, n_reads, total_mut)
