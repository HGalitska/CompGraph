# First lab for Computer Graphics course.
# Created by Olena Galitska. 21/02/2018 15:00


class Point:
    def __init__(self, x, y, num):
        self.x = float(x)
        self.y = float(y)
        self.num = num
        self.w_in = 0
        self.w_out = 0


class Edge:
    def __init__(self, start, end, num):
        self.start = start
        self.end = end
        self.num = num
        self.weight = 0


def sum_weight(array):
    result = 0
    for edge in array:
        result = result + edge.weight
    return result


def leftmost_edge(edg, ver):
    result = -1
    for edge in edg:
        if result == -1:
            result = edge
        else:
            if edge.end.x < result.end.x:
                result = edge
    return result


v0 = Point(11, 2,  0)
v1 = Point(19, 4,  1)
v2 = Point(7,  7,  2)
v3 = Point(11, 7,  3)
v4 = Point(19, 11, 4)
v5 = Point(11, 12, 5)
v6 = Point(17, 15, 6)
v7 = Point(3,  14, 7)
v8 = Point(8,  19, 8)
vertices = [v0, v1, v2, v3, v4, v5, v6, v7, v8]

e0 = Edge(v0, v2, 0)
e1 = Edge(v0, v3, 1)
e2 = Edge(v0, v4, 2)
e3 = Edge(v0, v1, 3)
e4 = Edge(v1, v4, 4)
e5 = Edge(v2, v3, 5)
e6 = Edge(v2, v7, 6)
e7 = Edge(v2, v5, 7)
e8 = Edge(v3, v5, 8)
e9 = Edge(v3, v4, 9)
e10 = Edge(v4, v5, 10)
e11 = Edge(v4, v6, 11)
e12 = Edge(v5, v6, 12)
e13 = Edge(v5, v8, 13)
e14 = Edge(v7, v8, 14)
e15 = Edge(v6, v8, 15)
edges = [e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15]


# for every vertex create a list of in- and outgoing edges
edgesIn = []
edgesOut = []

for v in vertices:
    edgesIn.insert(v.num, [])
    edgesOut.insert(v.num, [])

for e in edges:
    out = e.start.num
    into = e.end.num
    edgesOut[out].append(e)
    edgesIn[into].append(e)
    e.weight = 1

# weight balancing

n = len(vertices)

for i in range(1, n - 1):
    vertices[i].w_in = sum_weight(edgesIn[i])
    vertices[i].w_out = sum_weight(edgesOut[i])
    d1 = leftmost_edge(edgesOut[i], vertices)
    print(d1.num + 1)
    if vertices[i].w_in > vertices[i].w_out:
        d1.weight = vertices[i].w_in - vertices[i].w_out + 1
print("")
for i in range(n - 1, 1, -1):
    vertices[i].w_in = sum_weight(edgesIn[i])
    vertices[i].w_out = sum_weight(edgesOut[i])
    d2 = leftmost_edge(edgesIn[i], vertices)
    print(d2.num + 1)
    if vertices[i].w_out > vertices[i].w_in:
        d2.weight = vertices[i].w_out - vertices[i].w_in + d2.weight

# for v in vertices:
#      print(str(v.num) + " : " + str(v.w_in) + " : " + str(v.w_out))
#      print(edgesIn[v.num])
#      print(edgesOut[v.num])

# print("")
# for e in edges:
#      print(e.weight)


# chains creation

