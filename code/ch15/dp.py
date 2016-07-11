from operator import itemgetter
from itertools import product
import random

# 6.1 vazirani
def max_sub(ls):
    # for j in {2,..,n} consider contiguous sequences
    # ending exactly j. concentrate on the bellman-ford equation:
    # max_end_here = either add the current value or restart the count
    max_here = max_so_far = ls[0]
    l = r = 0
    ml,mr = l,r
    for j,v in enumerate(ls[1:],start=1):
        l,r,max_here = max((l,j,max_here+v),(j,j,v),key=itemgetter(2))
        ml,mr,max_so_far = max((ml,mr,max_so_far),(l,r,max_here),key=itemgetter(2))

    return ml,mr,max_so_far


# 6.2 vazirani
# the optimal solution for kth day uses the optimal solution to the k-1th day?
# maybe? or maybe the optimal route to a_n use the optimal route to a_n-1? no
# optimal route a_n after including cities up to a_j
# bellman-ford equation is
# you either stop at a_j or continue on from the last place that was stopped to construct
# solution z_n-1
#
# no. for every hotel j compute the minimum cost hotel to get to it from
# cost(j) = min[(200-(aj-a))^2+cost(i)]
# the overlapping problems are getting from 0 to hotel j most efficiently
# the only difficulty is mining over possible stops

def hotels(ls):
    cost = len(ls)*[None]

    cost[0] = 0
    for i in range(1,len(ls)):
        cost[i] = min([(200-(ls[i]-ls[j]))**2 + cost[j] for j in range(i)])

    return cost[-1]

# this is very similar to the above problem. you can think of
# picking which hotels as stops on a road trip with an infinite penalty
# if you stop within k miles, and the task is to maximum total something
# instead of minimize. the overlapping problems are maximum profit
# after considering upto hotel j, except for each case you need to check
# the constraint. also it's possible that just having hotel i is more
# profitable
def yuckdonalds(mi,pi,k):
    # P[i] = max_j<i(P[j]+a(i,j)p_i,pi)
    profit = len(ls)*[None]

    cnrt = lambda x,y: 1 if abs(x-y)>k else 0
    profit[0] = pi[0]
    for i in range(1,len(ls)):
        max([profit[j]+cnrt(mi[i],mi[j])*pi[i] for j in range(i)]+[pi[i]])


#6.4 vazirani
# prefixes are the subproblems: for every prefix A[1..j] loop from  1..k..j checking if A[1..k] can be split
# and if A[k+1..j] is in the dict

#6.5 vazirani
# there are only 7 different tilings per column and each column is only "compatible" with a a few other forward
# columns. use greedy approach but only over compatible column types (not really dp)
if __name__ == '__main__':


    ls = random.sample(range(10000),10)
    # ls = [42, ch31, -48, 62, -3, 61, -83, 80, -18, 87]
    # tup1 = max([(i,j,sum(ls[i:j+1])) for i in range(10) for j in range(10)],key=itemgetter(2))
    # tup2 = max_sub(ls)
    # print(ls,tup1,tup2,sep='\n')
    print(hotels(ls))