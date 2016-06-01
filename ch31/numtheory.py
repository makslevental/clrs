import random


def euclidsaglorec(a,b):
    a,b = max(a,b), min(a,b)
    if b == 0:
        return a,1,0
    else:
        d,x,y = euclidsaglorec(a%b,b)
        x,y = y, x-(a//b)*y
        return d,x,y

def euclidsagloiter(a,b):
    flip = b > a
    a,b = max(a,b), min(a,b)

    x0,y0,x1,y1 = 1,0,0,1
    while b !=0:
        q,a,b = a//b,b,a%b
        x0,x1 = x1,x0-q*x1
        y0,y1 = y1,y0-q*y1

    if flip:
        x0,y0 = y0,x0

    return a,x0,y0

def lcm(a,b):
    return a*b/euclidsagloiter(a,b)

def modlinearsol(a,b,n):
    d,x,y = euclidsagloiter(a,n)
    xs = []
    if b%d == 0:
        x0 = (x*(b/d)) % n
        for i in range(d):
            xs.append( (x0 + i*(n/d)) % n )
    return xs



def floyd(f, x0):
    # Main phase of algorithm: finding a repetition x_i = x_2i.
    p1 = f(x0) # f(x0) is the element/node next to x0.
    p2 = f(f(x0))
    while p1 != p2:
        p1 = f(p1)
        p2 = f(f(p2))

    # Find the position μ of first repetition.
    mu = 0
    p2 = x0
    while p1 != p2:
        p1 = f(p1)
        p2 = f(p2)   # Hare and tortoise move at same speed
        mu += 1

    # Find the length of the shortest cycle starting from x_μ
    lam = 1
    p2 = f(p1)
    while p1 != p2:
        p2 = f(p2)
        lam += 1

    return lam, mu

def pollardrho(n):
    x0 = random.randint(0,n-1)
    f = lambda x: (x**2+1)

    p1 = f(x0) # f(x0) is the element/node next to x0.
    p2 = f(f(x0))
    while True:
        t = abs(p1-p2)
        if 1 < euclidsagloiter(t,n) < n:
            print(t)
        p1 = f(p1)
        p2 = f(f(p2))

    # how to dynamically update so that you're
    # factoring smaller and smaller numbers

if __name__ == '__main__':
    # print(euclidsaglorec(99,78))
    # print(euclidsagloiter(99,78))
    print(floyd(lambda x: (x**2 -1)%73 ,2))
