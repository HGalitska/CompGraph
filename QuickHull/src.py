import matplotlib.pyplot as plt


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "(" + str(self.x) + " ; " + str(self.y) + ")"


hull = []


def read_points(file_name):
    points_list = []
    input_array = open(file_name).read().split()

    i = 0
    while i < len(input_array):
        new_point = Point(int(input_array[i]), int(input_array[i + 1]))
        points_list.append(new_point)
        i += 2
    return points_list


def distance(p1, p2, p):
    outer_product = (p.x - p1.x) * (p2.y - p1.y) - (p.y - p1.y) * (p2.x - p1.x)
    return abs(outer_product)


def on_side(p1, p2, p):
    outer_product = (p.x - p1.x) * (p2.y - p1.y) - (p.y - p1.y) * (p2.x - p1.x)

    if outer_product > 0:
        return 1
    if outer_product < 0:
        return -1
    return 0


def quick_hull(points, n, p1, p2, side):
    inner_point = None
    max_distance = 0

    for point in points:
        dist = distance(p1, p2, point)
        if dist > max_distance and on_side(p1, p2, point) == side:
            max_distance = dist
            inner_point = point

    if inner_point is None:
        if p1 not in hull:
            hull.append(p1)
        if p2 not in hull:
            hull.append(p2)
        return

    quick_hull(points, n, inner_point, p1, -1 * on_side(inner_point, p1, p2))
    quick_hull(points, n, inner_point, p2, -1 * on_side(inner_point, p2, p1))


def find_hull(points, n):
    if n < 3:
        print("Convex hull can be built only for >= 3 points")
        return

    min_x = min(points, key=lambda point: point.x)
    max_x = max(points, key=lambda point: point.x)

    quick_hull(points, n, min_x, max_x, 1)
    quick_hull(points, n, min_x, max_x, -1)

    for point in hull:
        print(point)
    return


def main():
    points = read_points("points.txt")
    n = len(points)

    for point in points:
        plt.plot(point.x, point.y, 'g^')

    find_hull(points, n)
    for point in hull:
        plt.plot(point.x, point.y, 'ro')
    plt.axis([-10, 10, -10, 10])
    plt.show()
    return


main()
