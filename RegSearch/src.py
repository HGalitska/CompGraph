# Third lab for Computer Graphics course.
# Created by Olena Galitska. 26/03/2018 13:26


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "(" + str(self.x) + " ; " + str(self.y) + ")"


class Interval:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def __repr__(self):
        return str(self.begin) + " -> " + str(self.end)


class Node:
    def __init__(self, interval, left_son, right_son):
        self.interval = interval
        self.left_son = left_son
        self.right_son = right_son
        self.in_intervals = []

    def __repr__(self):
        return "{" + str(self.interval) + " l:" + str(self.left_son) + " r:" + str(self.right_son) + str(
            self.in_intervals) + "}"


def read_points(file_name):
    points_list = []
    input_array = open(file_name).read().split()

    i = 0
    while i < len(input_array):
        points_list.append(Point(int(input_array[i]), int(input_array[i + 1])))
        i += 2
    return points_list


def insert(root, i):
    if root is None:
        return Node(i, None, None)

    b = root.interval.begin
    e = root.interval.end
    if i.begin <= b and i.end >= e:
        root.in_intervals.append(i)
    if i.begin <= (e + b) / 2:
        root.left_son = insert(root.left_son, i)
    if i.end > (e + b) / 2:
        root.right_son = insert(root.right_son, i)
    return root


def make_intervals(array):
    result = []
    size = len(array)
    for i in range(size - 1):
        new_interval = Interval(array[i].x, array[i + 1].x)
        result.append(new_interval)
    return result


def inorder(root):
    if root is None:
        return

    inorder(root.left_son)
    nodes.append(root)
    inorder(root.right_son)


points = read_points("points.txt")
region = read_points("region.txt")

n = len(points)

intervals = make_intervals(points)

tree_root = Node(Interval(0, 14), None, None)
for i in range(0, len(intervals)):
    tree_root = insert(tree_root, intervals[i])

region_interval = Interval(region[0].x, region[1].x)
tree_root = insert(tree_root, region_interval)

nodes = []
inorder(tree_root)
for i in range(0, len(nodes)):
    if region_interval in nodes[i].in_intervals:
        print(nodes[i])
