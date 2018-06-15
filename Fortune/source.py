# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import cmath
import numpy as np


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "(" + str(self.x) + " ; " + str(self.y) + ")"


# class BeachLineNode:
#     def __init__(self, data):
#         self.left = None
#         self.right = None
#
#         # парабола (задається рівнянням директриси та фокусу)
#         self.data = data
#
#     def insert(self, data):
#         # Compare the new value with the parent node
#         if self.data:
#             if data < self.data:
#                 if self.left is None:
#                     self.left = BeachLineNode(data)
#                 else:
#                     self.left.insert(data)
#             elif data > self.data:
#                 if self.right is None:
#                     self.right = BeachLineNode(data)
#                 else:
#                     self.right.insert(data)
#         else:
#             self.data = data
#
#     def print_tree(self):
#         if self.left:
#             self.left.print_tree()
#         print(self.data),
#         if self.right:
#             self.right.print_tree()
#
#     @staticmethod
#     def min_value_node(node):
#         current = node
#
#         while current.left is not None:
#             current = current.left
#
#         return current
#
#     def delete_node(self, root, key):
#
#         if root is None:
#             return BeachLineNode(key)
#
#         if key < root.data:
#             root.left = self.delete_node(root.left, key)
#
#         elif key > root.key:
#             root.right = self.delete_node(root.right, key)
#
#         else:
#             if root.left is None:
#                 temp = root.right
#                 # root = None
#                 return temp
#
#             elif root.right is None:
#                 temp = root.left
#                 # root = None
#                 return temp
#
#             temp = self.min_value_node(root.right)
#
#             root.key = temp.key
#
#             root.right = self.delete_node(root.right, temp.key)
#
#         return root


# функція для зчитування точок з текстового файлу
def read_points(file_name):
    points_list = []
    input_array = open(file_name).read().split()

    i = 0
    while i < len(input_array):
        new_point = Point(float(input_array[i]), float(input_array[i + 1]))
        points_list.append(new_point)
        i += 2
    return points_list


def quadratic_equation(a, b, c):
    delta = (b ** 2) - (4 * a * c)
    solution1 = (-b - cmath.sqrt(delta)) / (2 * a)
    solution2 = (-b + cmath.sqrt(delta)) / (2 * a)

    return solution1, solution2


def handle_point_event(point, sweep_line):
    print("point event at (" + str(point) + " " + str(sweep_line) + ")")


def handle_circle_event(point, sweep_line):
    print("circle event at (" + str(point) + " " + str(sweep_line) + ")")


def check_events(points, sweep_line):
    points = sorted(points, key=lambda p: p.x)
    for i in range(0, len(points)):
        if sweep_line == points[i].y:
            handle_point_event(points[i], sweep_line)

    for j in range(1, len(points) - 1):
        cur_point = points[j]
        prev_point = points[j - 1]
        next_point = points[j + 1]

        if prev_point.y == sweep_line or next_point.y == sweep_line:
            continue
        intersect = intersect_parabolas(prev_point, next_point, sweep_line)
        print(intersect)
        if points_distance(cur_point, intersect) == intersect.y - sweep_line:
            handle_circle_event(cur_point, sweep_line)


def intersect_parabolas(f1, f2, k):
    a1 = f1.x
    b1 = f1.y
    a2 = f2.x
    b2 = f2.y

    a = b2 - b1
    b = 2 * (a1 * b1 - a1 * b2 + a1 * k - a2 * k)
    c = a1 * a1 * (b2 - k) + a2 * a2 * (k - b1) - (b2 - b1) * (b1 - k) * (b2 - k)

    x1, x2 = np.real(quadratic_equation(a, b, c))

    y = 0
    x = 0
    if a1 < x1 < a2:
        x = x1
    elif a1 < x2 < a2:
        x = x2

    y = 0.5 * ((x - a1) ** 2 / (b1 - k) + (b + k))

    return Point(x, y)


def points_distance(p1, p2):
    return cmath.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)


def main():
    points = read_points("points.txt")
    points = sorted(points, key=lambda p: p.y)
    print(points)
    n = len(points)

    sweep_line = points[n - 1].y

    xs = []
    ys = []
    for point in points:
        xs.append(point.x)
        ys.append(point.y)

    plt.axis([-15, 15, -15, 15])

    i = 0
    maxim = sweep_line - points[0].y
    while i < maxim + 3:
        # plt.plot(xs, ys, 'ko', ms=1)
        above_points = []
        for point in points:
            if point.y >= sweep_line:
                above_points.append(point)

        # print(above_points)
        check_events(above_points, sweep_line)
        sweep_line -= 1
        # plt.plot([-15, 15], [sweep_line, sweep_line], '-b')
        # plt.show()
        i += 1


main()
