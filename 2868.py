import sys
import math 
A,B,V = list(map(int,sys.stdin.readline().split()))

day = (V-A)/(A-B)

print(math.ceil(day)+1)