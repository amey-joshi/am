import math

def prob_of_wait(E, m):
    """
    E:      traffic
    m:      # agents.
    Reference: https://en.wikipedia.org/wiki/Erlang_(unit)
    """ 
    p = 1
               
    if m > E:   
        try:
            numerator = E**m/math.factorial(m) * m/(m - E)
            denominator = 0

            for i in range(m):
                denominator += E**i/math.factorial(i)

            denominator += numerator

            p = numerator/denominator
        except OverflowError:
            print(f'Overflow due to E = {E}, m = {m}')
        
    return p

def calculate_ASA(wait_prob, mu, nagents, E):
    a_large_number = 1000
    
    if nagents > E:
        return wait_prob * mu/(nagents - E) * time_window_size
    else:
        return a_large_number
    
def find_nagents(E, m):
    start = m
             
    if not math.isnan(E):
        threshold = 0.8
        max_iter = m
        count = 0
        while (prob_of_wait(E, start) > threshold) and (count < max_iter):
            start += 1
            count += 1   
            
        if count == max_iter:
            print(f'Max iter reached for E = {E}, m = {m}.')
        
    return start

def find_nagents_1(E, m):
    start = m
             
    if not math.isnan(E):
        threshold = 0.8
        while prob_of_wait(E, start) > threshold:
            start += 1
            
    return start
    :q
