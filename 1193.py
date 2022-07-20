a = int(input())
num = 0 
cnt = 1  

while a > num :
    num += cnt 
    cnt += 1 

b = a - (num- (cnt-1))

if cnt % 2 == 0 :
     print(str(cnt-b)+'/'+str(b))
else:
    print(str(b)+'/'+str(cnt-b))

