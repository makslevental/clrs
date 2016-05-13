

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

# Recall: Two line segments can only intersect if they are
# horizontal neighbors