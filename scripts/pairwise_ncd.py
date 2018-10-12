import sys
import lzma
import bz2
import zlib
import getopt
from sklearn.cluster import AgglomerativeClustering
import sys
import argparse
import os
import bz2
import gzip


def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-x', '--seq_x', help="sequence 1", 
		type=str, required=True)
	parser.add_argument('-y', '--seq_y', help="sequence 2", 
		type=str, required=True)
	parser.add_argument('-c', '--compression', help="compression algorithm", 
		type=str,choices=['lzma', 'gzip', 'bzip2', 'zlib'], required=True)
	args = parser.parse_args()
	return args

def bwt(string):
	"""
	Code for Burrows-Wheeler Transformation. The code is adapted from Rosetta Code.
	"""
	s = "\002" + s + "\003"  
    table = sorted(s[i:] + s[:i] for i in range(len(s)))  
    last_column = [row[-1:] for row in table]
    return "".join(last_column) 
	

#given 2 sequence strings, returns sequences + concatenation as an object of bytes
def return_byte(sequence1, sequence2):
    seq1 = bytes(sequence1, 'utf-8')
    seq2 = bytes(sequence2, 'utf-8')
    seqconcat = concat(seq1, seq2)
    return(seq1, seq2, seqconcat)

#compresses input sequence using lempel-ziv markov algorithm
def compress_lzma(sequence):
    #lzma requires Python 3.
    lz = lzma.compress(sequence)
    return lz


def compress_gzip(sequence: bytes) -> bytes:
    return gzip.compress(sequence)

def compress_bzip2(sequence):
	return bz2.compress(sequence)

def compress_zlib(sequence):
	return zlib.compress(sequence)

def compress_lz4framed(sequence):
	return lz4framed.compress(sequence)

#input
def compressed_size(sequences, algorithm):
	if algorithm == "lzma":
		compressed_seq1 = compress_lzma(sequences[0])
		compressed_seq2 = compress_lzma(sequences[1])
		compressed_seqconcat = compress_lzma(sequences[2])
	if algorithm == "gzip":
		compressed_seq1 = compress_gzip(sequences[0])
		compressed_seq2 = compress_gzip(sequences[1])
		compressed_seqconcat = compress_gzip(sequences[2])
	if algorithm == "bzip2":
		compressed_seq1 = compress_bzip2(sequences[0])
		compressed_seq2 = compress_bzip2(sequences[1])
		compressed_seqconcat = compress_bzip2(sequences[2])
	if algorithm == "zlib":
		compressed_seq1 = compress_zlib(sequences[0])
		compressed_seq2 = compress_zlib(sequences[1])
		compressed_seqconcat = compress_zlib(sequences[2])
	if algorithm == "lz4":
		compressed_seq1 = compress_lz4framed(sequences[0])
		compressed_seq2 = compress_lz4framed(sequences[1])
		compressed_seqconcat = compress_lz4framed(sequences[2])
	compressed_seq1_size = sys.getsizeof(compressed_seq1)
	compressed_seq2_size = sys.getsizeof(compressed_seq2)
	compressed_seqconcat_size = sys.getsizeof(compressed_seqconcat)
	return(compressed_seq1_size, compressed_seq2_size, compressed_seqconcat_size)

#calculates NCD for 2 sequence sizes and their concatenation size
def compute_distance(x, y, cxy):
    if x > y:
        distance = ((cxy - y) / x)
    elif y > x:
        distance = ((cxy - x) / y)
    else:
        distance = ((cxy - x) / x)
    return distance

#concatenates two input sequences together
def concat(sequence1, sequence2):
	concat_genome = sequence1 + sequence2
	return concat_genome


def main(algorithm, seq_x, seq_y):
	#parse command line arguments
	inputfile1 = seq_x
	inputfile2 = seq_y
	outputfile = ''

	#error conditions: missing input and confliciting command line arguments
	if inputfile1=='' or inputfile2=='':
		print("Error: Missing input")
		sys.exit(3)

	#open input sequences, exits if file not found
	try:
		with open (inputfile1, "r") as myfile:
			seq1 = myfile.read()
	except:
		print('Error reading sequence 1')
		sys.exit(3)
	
	try:
		with open (inputfile2, "r") as myfile:
			seq2 = myfile.read()
	except:
		print('Error reading sequence 2')
		sys.exit(3)

	#convert input sequences into bytes
	sequences = return_byte(seq1, seq2)
	
	#compress input sequences
	sizes = compressed_size(sequences, algorithm)

	#compute ncd values
	ncd = compute_distance(sizes[0], sizes[1], sizes[2])
	print(ncd)

if __name__== "__main__":
	args = parse_arguments()
	algorithm = args.compression
	seq_x = args.seq_x
	seq_y = args.seq_y
	main(algorithm, seq_x, seq_y)
