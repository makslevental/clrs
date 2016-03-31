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

# 16.2-2
# k(w,j) = max({k(w-w_j,j-1)+v_j,k(w,j-1)})
# the overlapping problems are k(w-w_j,j-1) knapsack, i.e.
# the knapsack with just enough weight to include item j and having considered
# all j-1 items, or just k(w,j-1) the knapsack with the same weight but
def zero_one_knapsack_no_repet(ls, weight_lim):
    K = [[None for i in range(len(ls)+1)] for i in range(weight_lim+1)]

    # 0 weight means no objects
    for i in range(len(K[0])):
        K[0][i] = ([0,0],0)

    # 0 objects mean no objects at whatever weight (only problem is of course 0 indexing)
    for i in range(len(K)):
        K[i][0] = ([0,0],0)

    for w in range(weight_lim+1):
        for j,(vj,wj) in enumerate(ls,start=1):
            if wj <= w:
                K[w][j] = max(((w-wj,j-1),K[w-wj][j-1][1]+vj),([w,j-1],K[w][j-1][1]),key=itemgetter(1))
            else:
                K[w][j] = ([w,j-1],K[w][j-1][1])


    items = []
    item = K[-1][-1]
    while item[1] != 0:
        if type(item[0]) is tuple:
            items.append(item)
        item = K[item[0][0]][item[0][1]]

    items.reverse()
    return(K)


# 16.2-3
# wut? duh take the lightest object first

# 16.2-4
# duh go to the last stop before m miles, refill

# 16.2-5
# easy: sort the points. use the first point as the left endpoint of the first interval
# for the next point ask the question: is it covered? if not repeat.

# 16.2-6 use value density: value/weight

# 16.2-7 ummm pair the largest number in a with the largest numbers in b?


# 16.3-3 ummmmmmmmmmm i guess since adding equals the next you'll always skew to the right?

# 16.3-6 a full binary tree is uniquely defined by its preorder traversal. then represent each of the numbers using logn bits in the order they're seen by the preorder traversal

# 16.3-7 just create tri-valent nodes and then pop 3 at a time from the priorityqueue

# 16-1a exchange for as many of the decreasingly smaller denomination as possible
# 16-1b this is just base c representation of the amount of money
# 16-1c 4 3 1 to change 6
# 16-1d dynamic programming

# 16-1d dynamic programming table with 1..n (being the amount of money going down the side and 1..k going across the top
#   1       3       4
# 1 1       1       1
# 2 2       2       2
# 3 3   min_j{C[i-k_j,k_{j-1}]+1,C[i,k_{j-1}]}
# . 4
# . 5
# . 6
# n 7
def change(n,coins):
    num_coins = [[None for _ in range(len(coins))] for _ in range(n+1)]
    for i in range(len(coins)):
        num_coins[0][i] = 0
        num_coins[1][i] = 1

    for i in range(n+1):
        num_coins[i][0] = 0
        num_coins[i][1] = i

    for i in range(2,n+1):
        for j in range(2,len(coins)):
            if i-coins[j] < 0:
                num_coins[i][j] = num_coins[i][j-1]
            else:
                num_coins[i][j] = min([num_coins[i-coins[j]][j]+1, num_coins[i][j-1]])

    return(num_coins)


# 16-2a umm run them in order of shortest running time?
# 16-2b at every release it's like you've got some number of jobs competing (where the job running currently counts as a
# job that has some amount of time left, and similarly all the other paused jobs). just run the one to end soonest and
# reassess every release time. you can use a minheap. each job could be pushed and popped a total of k times, where k
# is the number of distinct release times so k^2logn

def change_alt(n,coins):
    num_coins = (n+1)*[None]
    num_coins[0] = 0
    for i in range(1,n+1):
        num_coins[i] = min([num_coins[i-coin]+1 for coin in filter(lambda x: x<=i,coins)])

    return(num_coins)

if __name__ == '__main__':
    # intervals = [(x,y) if x<=y else (y,x) for x,y in list(zip(sample(range(100),10),sample(range(100),8)))]
    # intervals.insert(0,(-1000,-999))
    # intervals.append((1000,10001))
    # intervals = list(zip(intervals,sample(range(1000),len(intervals))))
    # print(sorted(intervals,key=lambda x: x[0][1]))
    # intervals = [((13, 14), 561), ((20, 34), 388), ((35, 48), 721), ((39, 52), 525), ((46, 58), 210), ((65, 66), 681), ((22, 72), 623), ((35, 89), 756), ((38, 95), 760), ((71, 99), 67)]
    # s = [-1000,1,3,0,5,3,5,6,8,8,2,12,1000]
    # f = [-999,4,5,6,7,9,9,10,11,12,14,16,1001]
    # activity(list(zip(s,f)))
    # print(activity(intervals))
    # print(activity_greedy_iter(intervals))
    # print(weighted_activity(intervals))
    # print(zero_one_knapsack_no_repet(intervals,200))
    # a = sample(range(20),10)
    # b = reversed(sample(range(20),10))
    # print(reduce(lambda x,y:x*y[0]**y[1],zip(a,b),1))
    # print(reduce(lambda x,y:x*y[0]**y[1],zip(a,a),1))
    # print(change(100,[0,1]+sorted(list(sample(range(2,20),5)))))
    # change(74,[0,1,5,10,25])
    print(*change(11,[0,1,3,4]),sep='\n')
    print(change_alt(11,[1,3,4]))