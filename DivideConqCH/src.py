# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "(" + str(self.x) + " ; " + str(self.y) + ")"

# функція для зчитування точок з текстового файлу
def read_points(file_name):
    points_list = []
    input_array = open(file_name).read().split()

    i = 0
    while i < len(input_array):
        new_point = Point(int(input_array[i]), int(input_array[i + 1]))
        points_list.append(new_point)
        i += 2
    return points_list

# функція для визначення орієнтації трьох точок
def orientation(a, b, c):
    value = (b.y - a.y) * (c.x - b.x) - (c.y - b.y) * (b.x - a.x)
    if value == 0:
        return 0
    if value > 0:
        return 1
    if value < 0:
        return -1

# функція для знаходження опуклої оболонки методом Джарвіса
def get_jarvis_hull(points, n):
    if n <= 2:
        return

    result = []

    leftmost = points.index(min(points, key=lambda point: point.x))
    p = leftmost
    q = -1
    while q != leftmost:
        result.append(points[p])
        q = get_next_index(points, p)
        for i in range(n):
            if orientation(points[p], points[i], points[q]) == -1:
                q = i

        p = q

    return result

# функція для визначення наступного індексу при обході опуклої оболонки
def get_next_index(array, current_index):
    n = len(array)
    if current_index == n - 1:
        return 0
    return current_index + 1

# функція для визначення попереднього індексу при обході опуклої оболонки
def get_prev_index(array, current_index):
    n = len(array)
    if current_index == 0:
        return n - 1
    return current_index - 1

# функція для злиття опуклих оболонок
def merge_hulls(hull_1, hull_2):
    rightmost_1 = max(hull_1, key=lambda point: point.x)
    leftmost_2 = min(hull_2, key=lambda point: point.x)

    index_1 = hull_1.index(rightmost_1)
    index_2 = hull_2.index(leftmost_2)
    done = False

    while not done:
        done = True
        while orientation(hull_2[index_2], hull_1[index_1], hull_1[get_next_index(hull_1, index_1)]) >= 0:
            index_1 = get_next_index(hull_1, index_1)
        while orientation(hull_1[index_1], hull_2[index_2], hull_2[get_prev_index(hull_2, index_2)]) <= 0:
            index_2 = get_prev_index(hull_2, index_2)
            done = False

    upper_1 = index_1
    upper_2 = index_2
    index_1 = hull_1.index(rightmost_1)
    index_2 = hull_2.index(leftmost_2)
    done = False

    while not done:
        done = True
        while orientation(hull_1[index_1], hull_2[index_2], hull_2[get_next_index(hull_2, index_2)]) >= 0:
            index_2 = get_next_index(hull_2, index_2)
        while orientation(hull_2[index_2], hull_1[index_1], hull_1[get_prev_index(hull_1, index_1)]) <= 0:
            index_1 = get_prev_index(hull_1, index_1)
            done = True

    lower_1 = index_1
    lower_2 = index_2

    result = []

    index = upper_1
    result.append(hull_1[upper_1])
    while index != lower_1:
        index = get_next_index(hull_1, index)
        result.append(hull_1[index])

    index = lower_2
    result.append(hull_2[lower_2])
    while index != upper_2:
        index = get_next_index(hull_2, index)
        result.append(hull_2[index])

    print(result)

    return result

# основна функція для знаходження опуклої оболонки
def divide_and_conquer(points):
    n = len(points)
    if len(points) <= 5:
        return get_jarvis_hull(points, n)

    part_1 = []
    for i in range(0, n/2):
        part_1.append(points[i])
    part_2 = []
    for i in range(n/2, n):
        part_2.append(points[i])

    convex_hull_1 = divide_and_conquer(part_1)
    convex_hull_2 = divide_and_conquer(part_2)

    return merge_hulls(convex_hull_1, convex_hull_2)


def main():
    points = read_points("points.txt")
    points = sorted(points, key=lambda p: p.x)
    print(points)

    for point in points:
        plt.plot(point.x, point.y, 'go')

    hull = divide_and_conquer(points)

    xs = []
    ys = []
    for point in hull:
        xs.append(point.x)
        ys.append(point.y)

    plt.plot(xs, ys, '-ro')
    plt.plot([xs[0], xs[len(hull)-1]], [ys[0], ys[len(hull)-1]], '-ro')

    plt.axis([-10, 10, -10, 10])
    plt.show()
    return


main()
