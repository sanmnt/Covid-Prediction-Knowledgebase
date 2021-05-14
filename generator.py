import sys
def counter():
    f = open("numbers.txt","r")
    n = int(f.read())
    n = n +1
    write = open("numbers.txt", "w")
    print(n, file=write)
    return n

