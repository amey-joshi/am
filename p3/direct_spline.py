def b(n, m, k):
    if m == 0:
        raise ValueError('m cannot be zero')

    rv = 0; # Return value.
    if n == 0:
        if -m/2 <= k and k <= m/2:
            rv = 1
    else:        
        rv = (k/m + (n+1)/2)*c(n-1, m, k) + ((n+1)/2 - k/m)*c(n-1,m,k-m)
        rv = rv/n

    return rv

def c(n, m, k):
    if m == 0:
        raise ValueError('m cannot be zero')

    rv = 0; # Return value.
    if n == 0:
        if m - 2 <= k and k <= 0:
            rv = 1
    else:
        rv = (-k/m + (n+2)/2)*b(n-1, m, k-m) + (n/2 - k/m)*b(n-1,m,k)
        rv = rv/n

    return rv

