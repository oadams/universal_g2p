#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright 2019  Johns Hopkins University (Author: Matthew Wiesner)
# Apache 2.0

from __future__ import print_function
import argparse
import sys
import os
import codecs
import subprocess
import pdb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('test_words',
        help='words for G2P is used to derive pronunciations',
        type=str
    )
    parser.add_argument('train_words',
        help='words on which G2P was trained',
        type=str
    )
    parser.add_argument('transformed_words',
        help='test words that have oov characters romanized',
        type=str
    )

    args = parser.parse_args()

    print("Train graphemes")
    train_graphemes = set()
    with codecs.open(args.train_words, 'r', encoding='utf-8') as f:
        for l in f:
            for grapheme in l.strip():
                train_graphemes.add(grapheme) 

    print("Test graphemes")
    transformed = []
    with codecs.open(args.test_words, 'r', encoding='utf-8') as f:
        words = f.readlines()
    
    print("Transform graphemes")
    for idx_l, l in enumerate(words, 1):
        print('Word ', idx_l, ' of ', len(words))
        if set(w.strip()).isdisjoint(train_graphemes):
            new_word = u""
            for grapheme in l.strip():
                if grapheme not in train_graphemes:
                    ps = subprocess.Popen(['./uroman/bin/uroman.pl'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    ps.stdin.write(grapheme.encode('utf-8'))
                    romanized, _ = ps.communicate()
                    ps.stdin.close()
                    ps.stdout.close()
                    ps.stderr.close()
                    new_word += romanized.strip() 
                else:
                    new_word += grapheme
            transformed.append(new_word)
    
    with codecs.open(args.transformed_words, 'w', encoding='utf-8') as f:
        for w in transformed:
            print(w, file=f)

if __name__ == "__main__":
    main()

