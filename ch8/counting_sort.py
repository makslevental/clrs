import numpy as np

# only works for integers
def counting_sort_backwards(ls):
    k = max(ls)
    c = (k+1)*[0]
    for x in ls:
        c[x] += 1

    # c[i] is now the number occurrences of i

    for i in range(1,k+1):
        c[i] = c[i-1] + c[i]

    # c[i] is now the number of elements in the original list less or equal
    # to i

    b = len(ls)*[None]

    # this makes counting sort stable
    # traverse in reverse order because the count places the entry
    # into its last appearing position. in order forwards you'd have
    # count the number of elements /ahead/.
    for i in range(len(ls)-1,-1,-1):
        e = ls[i]
        b[c[e]-1] = e
        c[e] -= 1

    return b

def counting_sort_backwards_neg(ls):
    k = max(ls)
    kk = min(ls)
    r = k-kk+1
    c = r*[0]
    for x in ls:
        e = x-kk
        c[x-kk] += 1



    for i in range(1,r):
        c[i] = c[i-1] + c[i]


    b = len(ls)*[None]

    # this makes counting sort stable
    # traverse in reverse order because the count places the entry
    # into its last appearing position. in order forwards you'd have
    # count the number of elements /ahead/.
    for i in range(len(ls)-1,-1,-1):
        x = ls[i]
        e = x - kk
        b[c[e]-1] = x
        c[e] -= 1

    return b



# only works for positve integers
def counting_sort_forwards(ls):
    k = max(ls)
    c = (k+1)*[0]
    for x in ls:
        c[x] += 1

    # c[i] is now the number occurrences of i

    for i in range(k-1,0,-1):
        c[i] = c[i+1] + c[i]

    # c[i] is now how far back from the front i is

    b = len(ls)*[None]

    for e in ls:
        b[len(b)-c[e]] = e
        c[e] -= 1

    return b


if __name__ == '__main__':
    t = np.random.randint(-10,10,10)
    print(counting_sort_backwards_neg(t),sorted(t),sep='\n')


