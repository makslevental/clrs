

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



if __name__ == '__main__':
    # print(euclidsaglorec(99,78))
    # print(euclidsagloiter(99,78))
    print(modlinearsol(35,10,50))