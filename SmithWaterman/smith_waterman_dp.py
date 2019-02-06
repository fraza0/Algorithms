import numpy as np
from random import choice
import time

match_points = 5
mismatch_penalty = -3
gap_penalty = -4

def substitution_matrix(char_l, char_c):
    if char_l == char_c:
        return match_points
    else:
        return mismatch_penalty

def get_neighbors(matrix, l, c):
    leftNeighbor = matrix[l-1][c]
    topNeighbor = matrix[l][c-1]
    diagonalNeighbor = matrix[l-1][c-1]
    return (diagonalNeighbor, topNeighbor, leftNeighbor)

def smith_waterman_dp(seq1, seq2, l=1, c=1):
    if l==0 or c==0:
        return 0
    global iterations_count_matrix, iterations_count_back
    len_seq1, len_seq2 = len(seq1), len(seq2)
    score_matrix = np.zeros((len_seq1+1,len_seq2+1), dtype=np.int8)
    backtrack_matrix = np.zeros((len_seq1+1,len_seq2+1), dtype=np.int8)

    max_score, max_score_l, max_score_c = 0, 0, 0

    for l in range(1, len_seq1 + 1):
        for c in range(1, len_seq2 + 1):
            iterations_count_matrix+=1
            neighbors_score = get_neighbors(score_matrix,l,c)
            diagonal_score = neighbors_score[0] + substitution_matrix(seq1[l-1], seq2[c-1])
            top_score = neighbors_score[1] + gap_penalty
            left_score = neighbors_score[2] + gap_penalty
            score_matrix[l][c]=max(diagonal_score, top_score, left_score, 0)

            if score_matrix[l][c] == 0:
                backtrack_matrix[l][c] = 0 # end of path
            if score_matrix[l][c] == left_score:
                backtrack_matrix[l][c] = 1 # 1 move up
            if score_matrix[l][c] == top_score:
                backtrack_matrix[l][c] = 2 # move left
            if score_matrix[l][c] == diagonal_score:
                backtrack_matrix[l][c] = 3 # move diagonally
            if score_matrix[l][c] >= max_score:
                max_score_l, max_score_c = l, c
                max_score = score_matrix[l][c]

    
    align1, align2 = '', ''
    l,c = max_score_l,max_score_c

    #backtracing
    while backtrack_matrix[l][c] != 0:
        iterations_count_back+=1
        if backtrack_matrix[l][c] == 3:
            align1 += seq1[l-1]
            align2 += seq2[c-1]
            l -= 1
            c -= 1
        elif backtrack_matrix[l][c] == 2:
            align1 += '-'
            align2 += seq2[c-1]
            c -= 1
        elif backtrack_matrix[l][c] == 1:
            align1 += seq1[l-1]
            align2 += '-'
            l -= 1

    print(score_matrix)
    # print(score_matrix, '\n\n\n',backtrack_matrix)

    return align2[::-1]


# #Exemplo teste
# seq1, seq2 = "TGTTACGG", "GGTTGACTA"
# iterations_count_matrix, iterations_count_back = 0, 0
# score_matrix = np.zeros((len(seq1)+1,len(seq2)+1), dtype=np.int8)
# smith_waterman_dp(seq1, seq2)
# print(iterations_count_matrix)


alphabet = ['T','G','A','C']

seq1, seq2 = "", ""
max_iterations = 1

with open('sw_dp.txt', 'w') as out:
    out.write("Iterations: %s\n" %(max_iterations))
    out.write("Sequences Lenght\tIterations Matrix\tTime (sec.)\n")
    startTotalTime = time.time()
    steps = 10000
    for iter in range(1, max_iterations+1):
        for _ in range(steps):
            seq1+=choice(alphabet)
            seq2+=choice(alphabet)

        startTime = time.time()
        iterations_count_matrix, iterations_count_back = 0, 0
        smith_waterman_dp(seq1, seq2)
        endTime = time.time()
        print("%s\t\t\t\t\t%s\t\t\t\t\t%s" % (iter*steps, iterations_count_matrix, round(endTime-startTime, 3)))
        out.write("%s\t\t\t\t\t%s\t\t\t\t\t%s\n" % (iter*steps, iterations_count_matrix, round(endTime-startTime, 3)))

    out.write("Total Execution Time: %s secs." % (time.time()-startTotalTime))
    out.close()