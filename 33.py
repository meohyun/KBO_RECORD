# H, W, N, 세 정수를 포함하고 있으며 
# 각각 호텔의 층 수, 각 층의 방 수, 몇 번째 손님
import sys

T = int(sys.stdin.readline())

for _ in range(T):
    a = []
    H,W,N = list(map(int,sys.stdin.readline().split()))
    
    for i in range(H):
        for j in range(H):
            floor = 101+i+(100*j)
            a.append(floor)
    
    print(a[N-1])
    