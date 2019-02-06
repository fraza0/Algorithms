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

def smith_waterman_mem(l, c):
    global iterations_count_matrix, score_matrix, calls_count
    
    if score_matrix[l][c] != -1:
        return score_matrix[l][c]

    if l==0 or c==0:
        score_matrix[l][c] = 0
        return 0

    if score_matrix[l-1][c-1] != -1:
        diagonal_score = score_matrix[l-1][c-1] + substitution_matrix(seq1[l-1], seq2[c-1])
    else:
        calls_count+=1
        diagonal_score = smith_waterman_mem(l-1, c-1)+substitution_matrix(seq1[l-1], seq2[c-1])
    
    if score_matrix[l][c-1] != -1:
        top_score = score_matrix[l][c-1] + gap_penalty
    else:
        calls_count+=1
        top_score = smith_waterman_mem(l, c-1) + gap_penalty
    
    if score_matrix[l-1][c] != -1:
        left_score = score_matrix[l-1][c] + gap_penalty
    else:
        calls_count+=1
        left_score = smith_waterman_mem(l-1, c) + gap_penalty

    iterations_count_matrix+=1
    score_matrix[l][c] = max(diagonal_score, top_score, left_score, 0)
    return score_matrix[l][c]


alphabet = ['T','G','A','C']
seq1, seq2 = "", ""
max_iterations = 100

with open('sw_mem.txt', 'w') as out:
    out.write("Iterations: %s\n" %(max_iterations))
    out.write("Sequences Lenght\tIterations\tCalls\tTime (sec.)\n")
    print("Sequences Lenght\tIterations\tCalls\tTime (sec.)")
    startTotalTime = time.time()
    for seq_len in range(1, max_iterations+1):
        startTime = time.time()
        steps = 1
        for _ in range(steps):
            seq1+=choice(alphabet)
            seq2+=choice(alphabet)
        score_matrix = np.full([len(seq1)+1, len(seq2)+1], -1)
        iterations_count_matrix, calls_count = 0, 0
        smith_waterman_mem(len(seq1), len(seq2))
        endTime = time.time()
        print(seq_len*steps, '\t\t\t\t\t', iterations_count_matrix, '\t\t\t', calls_count, '\t\t', round(endTime-startTime, 3))
        out.write("%s\t\t\t\t\t%s\t\t\t%s\t\t%s\n" % (seq_len*steps, iterations_count_matrix, calls_count, round(endTime-startTime, 3)))
    out.write("Total Execution Time: %s secs." % (time.time()-startTotalTime))
    out.close()