from functools import reduce, cmp_to_key
from operator import itemgetter

from math import sqrt, ceil
from sortedcontainers import SortedListWithKey, SortedDict

def dist(x,y):
    return sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

def cross(v1,v2):
    x1,y1 = v1
    x2,y2 = v2
    # x1 y1
    # x2 y2
    return x1*y2 - y1*x2

def orient(l1,l2):
    # returns true if p2 is counterclockwise relative to p1
    p1,p2 = l1
    p3,p4 = l2
    v1 = p2[0] - p1[0],p2[1] - p1[1]
    v2 = p4[0] - p3[0],p4[1] - p3[1]
    return 1 if cross(v1,v2) > 0 else -1

def onseg(l,p):
    return (min(l[0][0],l[1][0]) <= p[0] <= max(l[0][0],l[1][0]) and
        min(l[0][1],l[1][1]) <= p[1] <= max(l[0][1],l[1][1]))


def segmentsintersect(l1,l2):
    p1,p2 = l1
    p3,p4 = l2
    # is p3 to the left or right of l1
    d1 = orient(l1,(p1,p3))
    # is p4 to the left or right of l1
    d2 = orient(l1,(p1,p4))
    # is p1 to the left or right of l2
    d3 = orient(l2,(p3,p1))
    # is p2 to the left or right of l2
    d4 = orient(l2,(p3,p2))

    # eg (d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)
    if d1*d2 < 0 and d3*d4 < 0:
        return True
    elif d1 == 0 and onseg(l1,p3):
        return True
    elif d2 == 0 and onseg(l1,p4):
        return True
    elif d3 == 0 and onseg(l2,p1):
        return True
    elif d4 == 0 and onseg(l2,p2):
        return True
    else:
        return False
# Recall: Two line segments can only intersect if they are
# horizontal neighbors
def anysegmentsintersect(segments):
    """returns True or False

    :param segments: line segments
    :type segments: list of pairs of tuples representing endpoints
    :return: whether there are any intersections

    """

    l_endpoints = {seg[0]:seg[1] for seg in segments}
    r_endpoints = {seg[1]:seg[0] for seg in segments}
    if (len(l_endpoints) < len(segments)) or (len(r_endpoints) < len(segments)):
        return True

    endpoints = sorted(reduce(lambda xs,x:xs+[(x[0],0,x[0][1])]+[(x[1],1,x[1][1])],segments,[]))

    sweep = SortedListWithKey(endpoints[0], key=itemgetter(1))

    for e in endpoints[1:]:
        if e in l_endpoints and e in r_endpoints:
            return True
        elif e in l_endpoints:
            sweep.add(e)
            # well this is dumb
            ind = sweep.index(e)
            try:
                if segmentsintersect((e,l_endpoints[e]), (sweep[ind+1],l_endpoints[sweep[ind+1]])):
                    return True
            except IndexError:
                try:
                    if segmentsintersect((e,l_endpoints[e]), (sweep[ind-1],l_endpoints[sweep[ind-1]])):
                        return True
                except IndexError:
                    pass
        elif e in r_endpoints:
            # well this is dumb
            ind = sweep.index(e)
            try:
                if (segmentsintersect((e,l_endpoints[e]), (sweep[ind+1],l_endpoints[sweep[ind+1]])) and
                    segmentsintersect((e,l_endpoints[e]), (sweep[ind-1],l_endpoints[sweep[ind-1]]))):
                    return True
            except IndexError:
                pass
            del sweep[ind]
    return False

def polar_compare(base):
    def comparator(p1,p2):
        u = (p1[0]-base[0],p1[1]-base[1])
        v = (p2[0]-base[0],p2[1]-base[1])
        c = cross(u,v)
        if c > 0:
            return 1
        elif c == 0:
            if dist(u,v) > 0:
                return 1
            else:
                return 0
        else:
            return 0

# starting with the southeastest point, traverse in polar order (farthest if tie)
# and throw away each point that isn't a left turn relative to the previous and the next
# pop the top if the angle between second to top and top and next is a right turn
def grahamscan(points):
    def south_east_cmp(p1,p2):
        if p1[1] < p2[1]:
            return 1
        elif p1[1] == p2[1]:
            if p1[0] < p2[0]:
                return 1
        else:
            return 0

    # this is fine here but could be O(n)
    south_eastest = sorted(points,key=south_east_cmp)[0]
    sorted_points = sorted(points,key=cmp_to_key(polar_compare(south_eastest)))

    stk = [south_eastest,sorted_points[0],sorted_points[1]]
    for p in sorted_points[2:]:
        while cross((stk[-1][0] - stk[-2][0],stk[-1][1]-stk[-2][1])
                    ,(p[0] - stk[-1][0],p[1]-stk[-1][1])) < 0:
            stk.pop()
        stk.append(p)

    return stk

def jarvismarch(points):
    j,southeastest = 0,points[0]
    for i,p in enumerate(points):
        if p[1] < southeastest[1]:
            j,southeastest = p
        elif p[1] == southeastest[1]:
            if p[0] < southeastest[0]:
                j,southeastest = p

    hull = [southeastest]
    endpoint = None
    while endpoint != southeastest:
        endpoint = points[0]
        for i,p in points[1:]:
            u = (p[0]-hull[-1][0],p[1]-hull[-1][1])
            v = (endpoint[0]-hull[-1][0],endpoint[1]-hull[-1][1])
            c = cross(u,v)
            if endpoint == hull[-1] or c > 0:
                endpoint = p
            elif c == 0:
                if dist(u,v) > 0:
                    endpoint = p
        if endpoint != southeastest:
            hull.append(endpoint)


def nearestpoints(points):
    def nearest_rec(xsorted,ysorted):
        if len(points) <= 3:
            x,y,z = xsorted
            nearest = min([(x,y,dist(x,y)),(x,z,dist(x,z)),(z,y,dist(z,y))],key=itemgetter(2))
            return nearest
        else:
            # divide array
            l = ceil(len(xsorted)/2)
            xsortedl = xsorted[:l]
            ysortedl = [p for p in ysorted if p in set(xsortedl)]
            xsortedr = xsorted[l:]
            ysortedr = [p for p in ysorted if p not in set(xsortedl)]
            l_nearest = nearest_rec(xsortedl,ysortedl)
            r_nearest = nearest_rec(xsortedr,ysortedr)

            # combine
            # the trick here is that we only need to look for points within delta (in either dimension)
            # of any point in the band. it turns out that at most 8 points are within delta (corners)
            # so we forget about delta and just check the nearest 8 points.
            delta = min(l_nearest[2],r_nearest[2])
            ywithindelta = [p for p in ysortedl+ysortedr if abs(p[0]-xsorted[l][0])<delta]
            deltap = (ywithindelta[0],ywithindelta[1],dist(ywithindelta[0],ywithindelta[1]))
            for i,p in enumerate(ywithindelta):
                deltap = min([(p,y,dist(p,y)) for y in ywithindelta[i:i+7]+deltap],itemgetter(2))

            return min(l_nearest,r_nearest,deltap,key=itemgetter(2))

    xsorted = sorted(points,key=itemgetter(0))
    ysorted = sorted(points,key=itemgetter(1))

    return nearest_rec(xsorted,ysorted)


if __name__ == '__main__':
    anysegmentsintersect([((9,10),(11,12)),((5,6),(7,8))])


# 33.1-3 pick your favorite comparison sort (quicksort eg) and use orient to do the comparison. this works
# since polar angles relative to a fix origin induce a total ordering on the points.

# 33.1-4 for each node do the above sort. then look for 2 vertices that have the same polar angle.

# 33.1-5 some of the points might be colinear, all of the points might be colinear. need to handle that.

# 33.1-6 compute intersection between p1p2 and p0_max{p1x,p2x}

# 33.1-7 check for intersections with all of the edges. edge case is when intersection is vertex (then it looks like
# there are two intersections but really only one). colinear with an edge check adds constant time.

# 33.1-8 take cross products? something with crossproducts. because the cross product is the area of the parallelpiped
# spanned by two vectors. then signs take car of overlap. yup sum the crossproducts of the vector to the vertices (wrt
# origin). don't forget to include the last vertex twice.

# 33.2-2 if a,b don't intersect then use cross product on their left endpoints. which ever is counter clockwise wrt
# to the other is higher (this is true no matter where the sweep line intersects). the trouble when a and b intersect
# is which side of the intersection are you on? multiply by denominators to get rid of division

# 33.2-4 use sweep line but just ignore intersections at vertices

# 33.2-5 same as above

# 33.2-6 two disks do not intersect if their centers for farther apart than r1+r2. "draw" the line segments that are parallel
# to the x axis that go through the centers of the disks and have lengths equal to twice the radii of the circles. then
# use the left points and right points as events in a sweep. add the lines to T according to height and add/remove when encountering
# (sort left to right breaking ties putting left endpoints before right endpoints). T should have always at most 1 element.
# you have to do this in the y direction too.
# 33.2-7 bentley-ottmann algo

# 33.2-8

# 33.2-9

# 33.3-3 duh. to find use the same trick as finding the diameter of a graph: pick an arbitrary point on the hull
# and find the farthest point on the convex hull and then find the farthest point from that point

# 33.3-4 um since the shape is specified by its vertices in counterclockwise order just run the main loop of graham scan
# on the vertices as given?

# 33.3-5 assume the convex hull of n-1 points is given by the vertices listed in counter clockwise order. if next point
# is on the interior of convex hull you can find this by the fact that walking along the convex hull pair of points by
# pair of points then going to the new point will consist of a left turn. if the next point is on the exterior then eventually
# this isn't true. wherever it's a right turn is where the new convex hull starts. then repeat the same process
# walk from the new point to each point following the break. the angles should increase and then decrease. when they
# decrease, the immediately prior point is the end of the new convex hull and the start of the old covnex hull.

# 33.3-6 essentially dp? convex hull of sorted 1-n is either convex hull of 1-{n-1} or includes nth point
# how to decide? something about angles? then the nlgn comes from the sort

# 33.4-2 something about the two sets of points at the intersection of the line wit the top and of the bounding box?

# 33.4-3 um just change dist? also number of points to be considered changes

# 33.4-4 same thing?

# 33-1a run jarvis match over and over again (removing after every run)

# 33-3 find the lower left point (ie convex hull). then sort by polar angle relative to that point. if last and next
# are opposite color then either line works. suppose not. go around keep track of how many ghostbustrs and ghosts you
# encounter (first point doesn't count). the last time the difference is 0 that's the line.

# 33-4 you can find overlapping lines by looking for intersections on XY plane. n^2. then use topological sort.
