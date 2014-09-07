#! /usr/bin/env python
import sys
import screed
import random
import fasta
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--error-rate', type=float, default=.01)
parser.add_argument('-r', '--read-length', type=int, default=100,
                    help="Length of reads to generate")
parser.add_argument('-C', '--coverage', type=int, default=50,
                    help="Targeted coverage level")
parser.add_argument("-S", "--seed", dest="seed", help="Random seed", type=int,
                    default=1)
parser.add_argument("--mutation-details", dest="mutation_details", help="Write detailed log of mutations here")

parser.add_argument('genome')
args = parser.parse_args()

args = parser.parse_args()

COVERAGE=args.coverage
READLEN=args.read_length
ERROR_RATE=args.error_rate

random.seed(args.seed)                  # make this reproducible, please.

record = iter(screed.open(args.genome)).next()

genome = record.sequence
len_genome = len(genome)

print >>sys.stderr, 'genome size:', len_genome
print >>sys.stderr, 'coverage:', COVERAGE
print >>sys.stderr, 'readlen:', READLEN
print >>sys.stderr, 'error rate:', ERROR_RATE

n_reads = int(len_genome*COVERAGE / float(READLEN))
reads_mut = 0
total_mut = 0

nucl = ['a', 'c', 'g', 't']

print >>sys.stderr, "Read in template genome {0} of length {1} from {2}".format(record["name"], len_genome, args.genome)
print >>sys.stderr, "Generating {0} reads of length {1} for a target coverage of {2} with a target error rate of 1 in {3}".format(n_reads, READLEN, COVERAGE, ERROR_RATE)

if args.mutation_details != None:
    details_out = open(args.mutation_details, "w")
else:
    details_out = None

for i in range(n_reads):
    start = random.randint(0, len_genome - READLEN)
    read = genome[start:start + READLEN].upper()

    # reverse complement?
    if random.choice([0, 1]) == 0:
        read = fasta.rc(read)

    # error?
    was_mut = False
    seq_name = "read{0}".format(i)
    read_mutations = 0
    for _ in range(READLEN):
        if ERROR_RATE > 0:
            while random.randint(1, int(1.0/ERROR_RATE)) == 1:
                pos = random.randint(1, READLEN) - 1
                orig = read[pos]
                new_base = random.choice(nucl)
                if orig.lower() == new_base:
                    continue
                
                if details_out != None:
                    print >>details_out, "{0}\t{1}\t{2}\t{3}".format(seq_name,
                                                          pos, orig, new_base)

                read = read[:pos] + random.choice(nucl) + read[pos+1:]
                was_mut = True
                total_mut += 1
                
        read_mutations += 1
    
    print '>{0} start={1},mutations={2}\n{3}'.format(seq_name, start, read_mutations, read)

print >>sys.stderr, "%d of %d reads mutated; %d total mutations" % \
    (reads_mut, n_reads, total_mut)
