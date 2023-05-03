T=5
Tf=1
it=20
alpha=0.95
k=1
while T >= Tf:
    for i in range(it):
        k+=1
    T=alpha*T
print(k)

