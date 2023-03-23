
for j in range(1,4):
    for i in range(1,27):
        a=str(i)
        b=str(j)
        filepath3 = "data/"+b+"/"+a+".txt"
        file3 = open(filepath3, 'r')
        arq3 = file3.read().splitlines()
        
