#!/bin/python

import sys
import random
import pandas as pd

sample_size = 500
self_choices = [1, 2, 3] # The choice 4 is added to the UI but it is same as 3.
seek_choices = [1, 2, 3]

def choice_2(seek1, p):
    """Get the second choice of partner.

        Second partner is chosen with a probability p.
        We ensure that the second choice is not the same as the first one.
        Return -1 if the second choice is not made.
    """
    if random.uniform(0, 1) > p:
        c = random.choice(seek_choices)
        if c == seek1:
            c = (c + 1) % 4
    else:
        c = -1

    return c

def choice_3(seek1, seek2, p):
    """Get the third choice of partner.

        Third partner is chosen with a probability p.
        We ensure that the third choice is not the same as the first two.
        Return -1 if the second choice is not made.
    """
    if seek2 != -1 and random.uniform(0, 1) > p:
        c = random.choice(seek_choices)
        if c == seek1 or c == seek2:
            c = 6 - (seek1 + seek2)
    else:
        c = -1

    return c

def generate(sample_size):
    self = random.choices(self_choices, k=sample_size)
    seek_1 = random.choices(seek_choices, k=sample_size)
    seek_2 = [choice_2(seek_1[i], 0.7) for i in range(sample_size)]
    seek_3 = [choice_3(seek_1[i], seek_2[i], 0.8) for i in range(sample_size)]
    ids  = [i for i in range(1, sample_size + 1)]

    df = pd.DataFrame(list(zip(ids, self, seek_1, seek_2, seek_3)), \
                      columns=['id', 'self', 'seek_1', 'seek_2', 'seek_3'])
    filename = f'sample_{sample_size}.csv'
    df.to_csv(filename, index=False, header=False)

def main():
    sample_size = 30

    if len(sys.argv) > 1:
        sample_size = int(sys.argv[1])

    generate(sample_size)

if __name__ == '__main__':
    main()


