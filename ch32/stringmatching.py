
def naive(text,pattern):
    for i in range(len(text)-len(pattern)):
        if text[i:len(pattern)] == pattern:
            return i
    return -1

def rabinkarp10(text,pattern):
    p = len(pattern)
    t = len(text)
    tt = hornersrule(text[0:0+p],10)
    pp = hornersrule(pattern,10)
    highonesdigit = 10**(p-1)
    for i in range(t-p+1):
        if pp == tt:
            return i
        else:
            tt = 10*(tt-highonesdigit*int(text[i]))+int(text[i+p])

    return -1

def rabinkarp(text,pattern,d,q):
    p = len(pattern)
    t = len(text)
    tt = hornersrule(text,d) % q
    pp = hornersrule(pattern,d) % q
    highonesdigit = d**(p-1) % q
    for i in range(t-p-1):
        if pp == tt:
            if pattern == text[i:i+p]:
                return i
        else:
            tt == (d*(tt-text[i]*highonesdigit) + int(text[i+p])) % q

    return -1

def finiteauto(text,trans,m):
    l = len(text)
    q = 0
    for i,t in enumerate(text):
        q = trans(q,t)
        if q == m:
            return i-m

# just do the dumb thing and try all p_qa
def transition(pattern,alphabet):
    p = len(pattern)
    trans = {}
    for q in range(p+1):
        for a in alphabet:
            k = min(p+1,q+2)
            s = pattern[:q]+a
            while pattern[:k] != s[-k:]:
                k -= 1
            trans[q,a] = k
    return trans



def hornersrule(x,base):
    result = 0
    for i in range(len(x)-1):
        result = base*(int(x[i])+result)

    result += int(x[-1])
    return result

def kmpmatch(text,pattern):
    # compute prefix function:
    # given that pattern[:q] == text[s:s+q]
    # what is the least shift  s' > s such that
    # there's another, possibly shorter match, i.e. for some k
    # pattern[:k] == text[s':s'+k]
    # where s'+k = s+q
    #
    # you can precompute such shifts by comparing pattern against itself
    # since text[s':s'+k] is part of t[s:s+q] and it already matches
    # pattern[:q] what we're actually looking for is the
    # longest proper prefix of pattern that is also a suffice of pattern[:q]
    # then the shift (since s'+k = s+q) s'=s+q-k. we want longest because
    # we want the next possible match.
    #
    # at each q store k (the number of matching characters at the new shift s', instead of s-s')
    # pi[q] = max {k: k<q pattern[:k] is a suffix of pattern[:q]
    pi = []
    k = 0
    pi[k] = k
    # essentially match pattern against pattern (compare to the loop below)
    for q,p in enumerate(pattern[1:]):
        while k > 0 and pattern[k+1] != p: # next character doesn't match
            k = pi[k] # skip back
        if pattern[k+1] == p: # if match then shift forward
            k += 1
        pi[q] = k



    q = 0
    for i,t in enumerate(text):
        while q > 0 and pattern[q+1] != t: # skip on first iteration but otherwise no match
            q = pi[q] # skip back
        if pattern[q+1] == t: # next letter matches
            q += 1
        if q == len(pattern):
            return i-len(pattern)





if __name__ == '__main__':
    print(str(hornersrule("123",10)))
    print(str(rabinkarp10("314159","159")))

# 32.1-2 you can advance the search as far as you've gotten in the check against P. i.e. if P=abcd and ab match but c fails
# then you can jump to start checking again where c failed.

# 32.1-3 the whole trick is rabinkarp essentially uses an incremental hash. this question hinges on how to update the
# incremental hash for matrices. so just find a 2d incremental hash.

# 32.3-4 create both independently and run both of them? take the cartesian product of the states and apply the transition functions
# coordinate wise

# 32.4-6 check sol4.ps

# 32.4-7 TT
