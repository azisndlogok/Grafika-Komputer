a=int(input("masukan nilai x1: "))
b=int(input("masukan nilai y1: "))
c=int(input("masukan nilai x2: "))
d=int(input("masukan nilai y2: "))

def kuadran(x,y):
    if (x>0 and y>0):
        titik = "kuadran I"
    elif (x<0 and y<0):
        titik = "kuadran III"
    elif (x<0 and y>0):
        titik = "kuadran II"
    else :
        titik = "kuadran IIII"
    return titik

jarak =((b-a)^2+(c-d)^2)**0.5
kuadran = kuadran(a,b)
print("")
print ("===HASIL===")
print (f"titik pertama: {a,b}")
print (f"titik kedua: {c,d}")
print (f"jarak antar titik: {jarak}")
print (f"titik pertama berada dalam {kuadran}")