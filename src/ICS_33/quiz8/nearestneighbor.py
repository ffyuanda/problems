import math

# Partition all values in the list in indexes left to right
#   inclusive, so that the leftmost values are <= the last value
#   and the rightmost values are > the last value.
# Return the index that the last value is swapped to, dividing
#   the <= and > values.
def partition(alist, left, right):
    def swap(i,j): alist[i],alist[j] = alist[j],alist[i] 
    pivot = alist[right]
    i = left
    for j in range(left,right):
        if alist[j] <= pivot:
            swap(i,j)          
            i += 1
    swap(i,right)          
    return i

# Returns the n-th smallest element of list within left..right inclusive
#  (i.e. 0 <= n < right).
def select(alist, n):
    left,right = 0, len(alist)-1
    while True:
        if left == right:
            return alist[left]
        pivot_index = partition(alist, left, right)
        if n == pivot_index:
            return alist[n]
        elif n < pivot_index:
            right = pivot_index - 1
        else:
            left  = pivot_index + 1
            
            

def closest_2d(alist):
    def dist(p1,p2): return math.sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    def min_none(*args): return min([x for x in args if x != None])
    if len(alist) < 2:
        return None # +infinity
    if len(alist) == 2:
        return dist(alist[0],alist[1])
     
    m = select([x for (x,_) in alist],len(alist)//2)
    s1,s2,s3 = [],[],[]
    for v in alist:
        if v[0] == m:
            s3.append(v)
        else:
            (s1 if v[0] < m else s2).append(v)
    if s1 == []:
        s1.append(s3[0])
        s2.extend(s3[1:])
    else:
        s2.append(s3[0])
        s1.extend(s3[1:])

    
    d1 = closest_2d(s1)
    d2 = closest_2d(s2)
    d = min_none(d1,d2)
    
    s1.sort(key = lambda p : p[1])
    s2.sort(key = lambda p : p[1])
    i,j = 0,0
    d3 = None # +infinity
    while True:
        while i != len(s1) and j != len(s2) and abs(s1[i][1]-s2[j][1]) > d:
            if s1[i][1] < s2[j][1]:
                i += 1
            else:
                j += 1
            
        if i == len(s1) or j ==len(s2):
            break;
        
        j1 = j
        while j1 < len(s2) and abs(s1[i][1]-s2[j1][1]) < d:
            if d3 == None or dist(s1[i],s2[j1]) < d3:
                d3 = dist(s1[i],s2[j1])
            j1 += 1
            
        i += 1            
    return min_none(d1,d2,d3)

