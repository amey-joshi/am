#!/bin/python

import random
import pandas as pd

sample_size = 10
self_choices = [1, 2, 3, 4]
seek_choices = [1, 2, 3]

self = random.choices(self_choices, k=sample_size)
seek = random.choices(seek_choices, k=sample_size)
ids  = [i for i in range(1, sample_size + 1)]

df = pd.DataFrame(list(zip(ids, self, seek)), columns=['id', 'self', 'seek'])
filename = f'sample_{sample_size}.csv'
df.to_csv(filename, index=False)

