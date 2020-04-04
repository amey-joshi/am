def b(n, m, k):
    rv = 0; # Return value.
    if n == 0:
        if -m/2 <= k and k <= m/2:
            rv = 1
    else:        
        rv = (k/m + (n+1)/2)*c(n-1, m, k) + ((n+1)/2 - k/m)*c(n-1,m,k-m)
        rv = rv/n

    print(f'b({n},{m},{k}) = {rv}')

    return rv

def c(n, m, k):
    rv = 0; # Return value.
    if n == 0:
        if m - 2 <= k and k <= 0:
            rv = 1
    else:
        rv = (-k/m + (n+2)/2)*b(n-1, m, k-m) + (n/2 - k/m)*b(n-1,m,k)
        rv = rv/n

    print(f'c({n},{m},{k}) = {rv}')

    return rv



##print("b(0,1,0) = ", b(0,0,0))
##print("c(0,1,0) = ", c(0,1,0))
##print("b(1,1,0) = ", b(1,1,0))
##print("c(1,1,0) = ", c(1,1,0))
##print("c(1,1,-1) = ", c(1,1,-1))
##print("c(1,1,1) = ", c(1,1,1))
##print("b(2,1,1) = ", b(2,1,1))
##print("b(2,1,0) = ", b(2,1,0))
##print("b(2,1,-1) = ", b(2,1,-1))
