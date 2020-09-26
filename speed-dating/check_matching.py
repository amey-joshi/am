#!/bin/python

import sys
import pandas as pd

def match(G, n1, n2):
    m1, m2 = False, False

    if (G.loc[G['id'] == n1]['self'].iloc[0] == G.loc[G['id'] == n2]['seek_1'].iloc[0]) or \
       (G.loc[G['id'] == n1]['self'].iloc[0] == G.loc[G['id'] == n2]['seek_2'].iloc[0]) or \
       (G.loc[G['id'] == n1]['self'].iloc[0] == G.loc[G['id'] == n2]['seek_3'].iloc[0]):
        m1 = True

    if (G.loc[G['id'] == n2]['self'].iloc[0] == G.loc[G['id'] == n1]['seek_1'].iloc[0]) or \
       (G.loc[G['id'] == n2]['self'].iloc[0] == G.loc[G['id'] == n1]['seek_2'].iloc[0]) or \
       (G.loc[G['id'] == n2]['self'].iloc[0] == G.loc[G['id'] == n1]['seek_3'].iloc[0]):
        m2 = True

    return (m2 and m2)

def check(gfile, mfile):
    G = pd.read_csv(gfile)
    n_errors = 0

    with open(mfile, 'r') as f:
        for line in f:
            nodes = [int(n.strip()) for n in line.replace('{','').replace('}','').split(',')] 
            n1, n2 = nodes[0], nodes[1]
            if not match(G, n1, n2):
                n_errors += 1

    print(f'There were {n_errors} errors.')

def main():
    if len(sys.argv) < 3:
        print('Usage: check_matching <sample file> <match file>')
        exit(-1)

    check(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()


