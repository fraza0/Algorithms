import numpy as np
from random import choice
import time
import sys

global seq1, seq2

match_points = 5
mismatch_penalty = -3
gap_penalty = -4

def substitution_matrix(char_l, char_c):
    if char_l == char_c:
        return match_points
    else:
        return mismatch_penalty

def smith_waterman_rec(l, c):
    global iterations_count_matrix
    if l==0 or c==0:
        return 0
    diagonal_score = smith_waterman_rec(l-1, c-1)+substitution_matrix(seq1[l-1], seq2[c-1])
    top_score = smith_waterman_rec(l, c-1) + gap_penalty
    left_score = smith_waterman_rec(l-1, c) + gap_penalty
    iterations_count_matrix+=1
    return max(diagonal_score, top_score, left_score, 0)



alphabet = ['T','G','A','C']
seq1, seq2 = "", ""
max_iterations = 13

with open('sw_rec.txt', 'w') as out:
    out.write("Iterations: %s\n" %(max_iterations))
    out.write("Sequences Lenght\t Calls\tTime (sec.)\n")
    # print("Sequences Lenght\t Calls\tTime (sec.)")
    startTotalTime = time.time()
    for seq_len in range(1, max_iterations+1):
        startTime = time.time()
        seq1+=choice(alphabet)
        seq2+=choice(alphabet)
        iterations_count_matrix=0
        smith_waterman_rec(len(seq1),len(seq2))
        endTime = time.time()
        # print(seq_len, '\t\t\t\t\t', iterations_count_matrix, '\t\t ', round(endTime-startTime, 3))
        out.write("%s\t\t\t\t\t%s\t\t %s\n" % (seq_len, iterations_count_matrix, round(endTime-startTime, 3)))
    out.write("Total Execution Time: %s secs." % (time.time()-startTotalTime))
    out.close()