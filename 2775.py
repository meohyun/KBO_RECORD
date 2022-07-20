import sys
T = int(sys.stdin.readline())

for _ in range(T):

    k = int(sys.stdin.readline())
    n = int(sys.stdin.readline())

    a = [[0]*(n+1) for _ in range(k+1)]

    for i in range(1,k+1):
        a[i][0] = 1
        for j in range(1,n+1):
            a[0][j] = j+1
            a[i][j] = a[i-1][j] + a[i][j-1]

    print(a[k][n-1])

        
        