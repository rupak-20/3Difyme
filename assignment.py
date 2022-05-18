# ----submitted by Rupak----

# Given a text file as input containing the input in the following format. Return the linear and circular distance

# sample input:
# cake make
# pod lot
# abc def
# xyz abc
# rail liar

# sample output:
# 10 10
# 20 14
# 9 9
# 69 9
# 28 28

import sys


# function to calculate linear and circular distance between the given two words
def distance(word1: str, word2: str) -> tuple:
    word1, word2 = word1.lower(), word2.lower()

    # if the length of the words are different then return
    if(len(word1) != len(word2)):
        print('skipping current line (words are of different length)')
        return ()

    dist_linear = 0
    dist_circular = 0

    for i in range(len(word1)):
        current = abs(ord(word1[i]) - ord(word2[i]))
        dist_linear += current
        dist_circular += min(current, 26 - current)

    return (dist_linear, dist_circular)


# driver code
if __name__ == '__main__':

    try:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
            for line in lines:
                word1, word2 = line.split()
                res = distance(word1, word2)
                print(res[0], res[1])

    # if file not found then print the following text
    except:
        print('text file not found')
