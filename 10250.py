import sys

T = int(sys.stdin.readline())

for _ in range(T):
    H,W,N = list(map(int,sys.stdin.readline().split()))
    
    # N이 H의 배수가 아닌경우에는 1~H-1층
    num = (N//H)+1 # 방번호
    floor = N % H # 층

    # 나머지가 0이된다는 것은 N은 H의 배수이기에 방번호는 몫이 되고 층은 꼭대기층인 H층이된다.
    if floor == 0:
        num = N//H
        floor = H 

    print(floor*100+num)
    


        