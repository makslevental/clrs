from random import sample
from operator import itemgetter, getitem
from collections import OrderedDict
from itertools import product
from functools import reduce
# activity selector
# max number of activities
# c[i,j] = c[i,k]+c[k,j]+1
# for the optimal k
# S_ij = set of activities that start after a_i ends finish before aj starts
# S_ij = (ai.f,aj.s)
# A_ij = maximal set of activities in S_ij

# i,j 2d matrix
def activity(ls):
    # sort by starting time
    # sort by ending time
    endtimels = list(sorted(ls,key=itemgetter(1)))
    endtimed = OrderedDict([(v,i) for i,v in enumerate(endtimels)])


    #matrix S[i,j] is set of intervals (ai.f,aj.s)
    # reduce(getitem,(1,2),S)
    # what's the efficient way to do this...?
    S = [[None for x in range(len(ls))] for y in range(len(ls))]
    A = [[None for x in range(len(ls))] for y in range(len(ls))]
    C = [['' for x in range(len(ls))] for y in range(len(ls))]
    for i,j in list(product(range(len(ls)),range(len(ls)))):
        # print(i,j)
        S[i][j] = list(filter(lambda x: endtimels[i][1]<=x[0] and x[1]<=endtimels[j][0],endtimels))



    # for i in range(len(ls)):
    #     S[i][-1].append(ls[-1])

    for i in range(len(ls)-1,-1,-1):
        for j in range(i,len(ls)):
            A[i][j] = max([(C[i][k]+C[k][j]+1,k) for k in [endtimed[v] for v in S[i][j]]]+[(0,-1)])
            jobs = S[i][j]
            key = [endtimed[v] for v in jobs]
            maxA = [C[i][k]+C[k][j]+1 for k in key]+[0]
            C[i][j] = max(maxA)

    job = A[0][-1][1]
    jobs = []
    while job != -1:
        jobs.append(job)
        job = A[0][job][1]

    return(list(reversed([endtimels[v] for v in jobs])))


# 16.1-4 interval-graph coloring
# duh sort by start time and then allocate to the first available lecture hall. if no lecture hall is available
# then open a new one. what does this have to do with graph coloring?

def activity_greedy_iter(ls):
    # pick the activity ending first then pick the activity the first compatible activity after that
    endtimels = list(sorted(ls,key=itemgetter(1)))
    endtimed = OrderedDict([(v,i) for i,v in enumerate(endtimels)])

    activities = [endtimels[0]]
    act = activities[0]
    for ac in endtimels[1:]:
        if act[1]<=ac[0]:
            activities.append(ac)
            act = ac

    return(activities[1:-1])

# 16.1-5
# max over weight? same bellman equation as for resource allocation. dummy. use the greedy algorithm. either
# the next job contributes to an optimal solution or it doesn't. if it does then the sub problem is maximum value
# job allocation strategy over jobs compatible with it. if it doesn't the just use prior value

def weighted_activity(ls):
    endtimels = list(sorted(ls,key=lambda x:x[0][1]))
    # p(j) highest index i that's comptabile with a_j
    p = len(endtimels)*[None]
    for i in range(len(ls)):
        j = -1
        while endtimels[j+1][0][1] <= endtimels[i][0][0]:
            j +=1
        p[i] = j

    opt = len(endtimels)*[0]
    opt[0] = (endtimels[0],-1)
    for i in range(1,len(endtimels)):
        # if job i is selected, then incompatible jobs p[i]+1,p[i]+2,...,j-1 cannot be used
        a = endtimels[i][1]+(opt[p[i]][1] if p[i] > -1 else 0)
        # if job i is not selected
        b = opt[i-1][1]
        # doing this wrong. recording the wrong backpointer thingy
        opt[i] = max(((endtimels[i][0],p[i]),a),(i-1,b),key=itemgetter(1))

    jobs = []
    for v in opt:
        if type(v[0]) is tuple:
            jobs.append(v[0][0])
    return((jobs,opt[-1][1]))


if __name__ == '__main__':
    intervals = [(x,y) if x<=y else (y,x) for x,y in list(zip(sample(range(100),10),sample(range(100),10)))]
    # intervals.insert(0,(-1000,-999))
    # intervals.append((1000,10001))
    intervals = list(zip(intervals,sample(range(1000),len(intervals))))
    # print(sorted(intervals,key=lambda x: x[0][1]))
    # intervals = [((13, 14), 561), ((20, 34), 388), ((35, 48), 721), ((39, 52), 525), ((46, 58), 210), ((65, 66), 681), ((22, 72), 623), ((35, 89), 756), ((38, 95), 760), ((71, 99), 67)]
    # s = [-1000,1,3,0,5,3,5,6,8,8,2,12,1000]
    # f = [-999,4,5,6,7,9,9,10,11,12,14,16,1001]
    # activity(list(zip(s,f)))
    # print(activity(intervals))
    # print(activity_greedy_iter(intervals))
    print(weighted_activity(intervals))