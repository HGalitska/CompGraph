# First lab for Computer Graphics course.
# Created by Olena Galitska. 21/02/2018 15:00
import math


class Point:
    def __init__(self, x, y, num):
        self.x = float(x)
        self.y = float(y)
        self.num = num
        self.w_in = 0
        self.w_out = 0

    def __repr__(self):
        return repr(self.num)


class Edge:
    def __init__(self, start, end, num):
        self.start = start
        self.end = end
        self.num = num
        self.weight = 0
        self.to = end.x
        self.rotation = math.atan2(end.y - start.y, end.x - start.x)

    def __repr__(self):
        return repr(self.num)


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


def sort_edges(array):
    return sorted(array, key=lambda edge: edge.rotation, reverse=True)


def create_chains(current_vertex, chain_number):
    edges_out_current = edges_out[current_vertex]
    for j in range(0, len(edges_out_current), 1):
        if 0 < j:
            chain_number = chain_number + 1
        if chain_number > 5:
            return 5
        chains[chain_number].append(edges_out_current[j].num)
        next_vertex = edges_out_current[j].end.num
        len_next = len(edges_out[next_vertex])
        if len_next > 1:
            for k in range(1, len_next):
                for edg in chains[chain_number]:
                    if edg not in chains[chain_number + k - 1]:
                        chains[chain_number + k - 1].append(edg)
        chain_number = create_chains(next_vertex, chain_number)
    return chain_number


def find(point):
    for p in range(0, num_chains, 1):
        for e in chains[p]:
            if edges[e].start.y < point.y < edges[e].end.y:
                point_vector = Point(point.x - edges[e].start.x, point.y - edges[e].start.y, -1)
                edge_vector = Point(edges[e].end.x - edges[e].start.x, edges[e].end.y - edges[e].start.y, -1)
                if math.atan2(point_vector.y, point_vector.x) > math.atan2(edge_vector.y, edge_vector.x):
                    return "Point is between chains " + str(p - 1) + " , " + str(p)
    return "Point is not inside graph"


v0 = Point(11, 2,  0)
v1 = Point(19, 4,  1)
v2 = Point(7,  7,  2)
v3 = Point(11, 7,  3)
v4 = Point(19, 11, 4)
v5 = Point(11, 12, 5)
v6 = Point(17, 14, 6)
v7 = Point(3,  15, 7)
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
edges_in = []
edges_out = []

for v in vertices:
    edges_in.insert(v.num, [])
    edges_out.insert(v.num, [])
vertices = sorted(vertices, key=lambda point: point.y)

for e in edges:
    out = e.start.num
    into = e.end.num
    edges_out[out].append(e)
    edges_in[into].append(e)
    e.weight = 1

# weight balancing

n = len(vertices)

for i in range(1, n - 1):
    vertices[i].w_in = sum_weight(edges_in[i])
    vertices[i].w_out = sum_weight(edges_out[i])
    d1 = leftmost_edge(edges_out[i], vertices)
    # print(d1.num + 1)
    if vertices[i].w_in > vertices[i].w_out:
        d1.weight = vertices[i].w_in - vertices[i].w_out + 1

for i in range(n - 1, 1, -1):
    vertices[i].w_in = sum_weight(edges_in[i])
    vertices[i].w_out = sum_weight(edges_out[i])
    d2 = leftmost_edge(edges_in[i], vertices)
    # print(d2.num + 1)
    if vertices[i].w_out > vertices[i].w_in:
        d2.weight = vertices[i].w_out - vertices[i].w_in + d2.weight
# chains creation

num_chains = sum_weight(edges_out[0])
chains = []
for j in range(num_chains):
    chains.insert(j, [])

sorted_edges = []
for v in edges_out:
    v = sort_edges(v)
    sorted_edges.append(v)

edges_out = sorted_edges

create_chains(0, 0)

point_to_find = Point(10, 8, -1)
print(find(point_to_find))
