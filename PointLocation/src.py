# First lab for Computer Graphics course.
# Created by Olena Galitska. 31/01/2018 15:22


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)


class Edge:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start = Point(start_x, start_y)
        self.end = Point(end_x, end_y)

    def is_upward(self, p):
        if self.start.y <= p.y < self.end.y:
            return True
        return False

    def is_downward(self, p):
        if self.end.y < p.y < self.start.y:
            return True
        return False

    def intersect(self, p):
        okay = True
        intersect_x = (self.end.x - self.start.x) * (p.y - self.start.y) / (self.end.y - self.start.y) + self.start.x
        if self.start.x <= intersect_x <= self.end.x or self.start.x > intersect_x > self.end.x:
            # exclude vertices if intersection:
            if self.start.y == p.y and intersect_x == self.start.x:
                okay = False
            if self.end.y == p.y and intersect_x != self.end.x:
                okay = False
        if okay:
            return intersect_x

# Hard coded polygon and point for testing.


e_0 = Edge(-1, -1, -3, 1)
e_1 = Edge(-3, 1, -3, 4)
e_2 = Edge(-3, 4, 1, 1)
e_3 = Edge(1, 1, 1, 4)
e_4 = Edge(1, 4, 3, 4)
e_5 = Edge(3, 4, 3, -1)
e_6 = Edge(3, -1, 1, -2)
e_7 = Edge(1, -2, -1, -1)
edges = [e_0, e_1, e_2, e_3, e_4, e_5, e_6, e_7]
point = Point(-1, -0.5)


# User input for polygon and point.
# edges = []
# n = input("How many edges does your polygon have?")
#
# for i in range(n):
#     print("Coordinates for edge " + str(i) + ":")
#     x_1 = input("x1: ")
#     y_1 = input("y1: ")
#     x_2 = input("x2: ")
#     y_2 = input("y2: ")
#     edges.insert(i, Edge(x_1, y_1, x_2, y_2))
#
# print("Coordinates for point to be located:")
# p_x = input("x: ")
# p_y = input("y: ")
# point = Point(p_x, p_y)


crossing_n = 0

for edge in edges:
    if edge.is_upward(point) or edge.is_downward(point):
        if point.x < edge.intersect(point):
            crossing_n += 1

print("Crossing number: " + str(crossing_n))
if crossing_n % 2 == 0:
    print("Point is outside the polygon.")
else:
    print("Point is inside the polygon.")
