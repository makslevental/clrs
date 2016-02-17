
# only works for integers
def counting_sort(ls):
    k = max(ls)
    c = k*[0]
    for x in ls:
        c[x] += 1

    # c[i] is now the number occurrences of i

    for i in range(1,k+1):
        c[i] = c[i-1] + c[i]

    # c[i] is now the number of elements in the original list less or equal
    # to i

    b = len(ls)*[None]

    for i in range(len(ls),-1,-1):
        e = ls[i]
        #
        b[c[e]] = e
        c[ls[i]] -= 1


