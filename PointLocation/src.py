# First lab for Computer Graphics course.
# Created by Olena Galitska. 31/01/2018 15:22


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def is_upward(self, p):
        if self.start.y <= p.y < self.end.y:
            return True
        return False

    def is_downward(self, p):
        if self.end.y < p.y < self.start.y:
            return True
        return False

    def intersect(self, p):
        x_1 = self.start.x
        x_2 = self.end.x
        y_1 = self.start.y
        y_2 = self.end.y

        intersect_x = (x_2 - x_1) * (p.y - y_1) / (y_2 - y_1) + x_1  # from line equation
        cross = Point(intersect_x, p.y)
        if self.start == cross or self.end == cross:
            return
        else:
            return intersect_x


def read_points(file_name):
    points = []
    input_array = open(file_name).read().split()

    i = 0
    while i < len(input_array):
        points.append(Point(int(input_array[i]), int(input_array[i + 1])))
        i += 2
    return points


vertices = read_points("polygon.txt")
num_vertices = num_edges = len(vertices)

edges = []
for j in range(num_edges):
    if j == num_edges - 1:
        edges.append(Edge(vertices[num_vertices - 1], vertices[0]))
        break
    edges.append(Edge(vertices[j], vertices[j + 1]))

test_points = read_points("points.txt")

k = 1
for point in test_points:
    min_x = min(vertices, key=lambda v: v.x).x
    max_x = max(vertices, key=lambda v: v.x).x

    if point.x < min_x or point.x > max_x:
        print(str(k) + ". Outside.")
        continue

    crossing_n = 0  # crossing number
    for edge in edges:
        if edge.is_upward(point) or edge.is_downward(
                point):  # if current edge is crossed by the ray starting at point
            if point.x < edge.intersect(point):  # and if intersection is on the right
                crossing_n += 1

    if crossing_n % 2 == 0:
        print(str(k) + ". Outside.")
    else:
        print(str(k) + ". Inside.")
    k += 1
    