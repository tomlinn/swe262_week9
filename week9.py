import sys, string
import numpy as np

# Read character
characters = np.array([' ']+list(open("pride-and-prejudice.txt").read())+[' '])


# Normalize
characters[~np.char.isalpha(characters)] = ' '
characters = np.char.lower(characters)


# Leetify
mydictionary = {"a": "4", "e": "3", "i": "1", "o": "0","u":"_"}
def leet(ch):
    if len(ch) == 1:
        return mydictionary.get(ch) if ch in "aeiou" else ch
    else:
        for c in mydictionary.keys():
            ch = ch.replace(c, mydictionary.get(c))
        return ch

# Leetify
characters = np.array(list(map(leet, characters)))

sp = np.where(characters == ' ')
sp2 = np.repeat(sp, 2)
w_ranges = np.reshape(sp2[1:-1], (-1, 2))
w_ranges = w_ranges[np.where(w_ranges[:, 1] - w_ranges[:, 0] > 2)]


words = list(map(lambda r: characters[r[0]:r[1]], w_ranges))
swords = np.array(list(map(lambda w: ''.join(w).strip(), words)))


#Remove stop words and Leetify
stop_words = np.array(list(set(open('stop_words.txt').read().split(','))))
stop_words = np.char.lower(stop_words)
stop_words = list(map(leet, stop_words))
ns_words = swords[~np.isin(swords, stop_words)]

# 2 grams
twogram = np.lib.stride_tricks.sliding_window_view(ns_words, 2)

#count the word occurrences
uniq, counts = np.unique(twogram, axis=0, return_counts=True)
combine = np.column_stack((uniq,counts))
wf_sorted = sorted(combine, key=lambda t: int(t[2]), reverse=True)

for w1,w2, c in wf_sorted[:5]:
    print(w1,w2, '-', c)
