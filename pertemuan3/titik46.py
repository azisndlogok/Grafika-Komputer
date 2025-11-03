x,y=(4,6)

for a in range (10):
    for b in range (10):
        if (a == x and b == y):
            print ("X",end="")
        else:
            print ("*",end="")
    print ("")