# -*- coding: utf-8 -*-
# Лабораторна робота 2.1: Локалізація точки на планарному розбитті, метод трапецій.
# Галіцька Олена ІС-3

import numpy

class Point:
    def __init__(self, x, y, num):
        self.x = float(x)
        self.y = float(y)
        self.num = num

    def __repr__(self):
        return str(self.num)


class Edge:
    def __init__(self, start, end, num):
        self.start = start
        self.end = end
        self.num = num

    def __repr__(self):
        return str(self.num)


class Node:
    LEAF_NODE = -1
    VERTEX_NODE = 1
    EDGE_NODE = 0

    def __init__(self, node_type, data):
        self.type = node_type
        self.data = data
        self.left_son = None
        self.right_son = None
        self.trap_num = 0

    def __repr__(self):
        if self.type == Node.LEAF_NODE:
            result_string = str(self.trap_num)
        else:
            result_string = "<" + str(self.type) + ", " + str(self.data) + "\n left:\n " + str(self.left_son) + "\n right:\n " + str(self.right_son) + "\n>"
        return result_string


def read_points(file_name):
    points = []
    input_array = open(file_name).read().split()

    i = 0
    v_num = 0
    while i < len(input_array):
        points.append(Point(float(input_array[i]), float(input_array[i + 1]), v_num))
        i += 2
        v_num += 1
    return points


def read_edges(file_name, vertices):
    edgs = []
    input_array = open(file_name).read().split()

    i = 0
    edge_num = 0
    while i < len(input_array):
        edgs.append(Edge(vertices[int(input_array[i])], vertices[int(input_array[i + 1])], edge_num))
        i += 2
        edge_num += 1
    return edgs


def crosses(edge, bottom_limit, top_limit):
    return edge.start.y <= bottom_limit and edge.end.y >= top_limit


def weight_of_node(node):
    if node is None:
        return 0
    if node.type == Node.LEAF_NODE:
        return 0
    else:
        if node.type < 1:
            result = float(weight_of_node(node.left_son) + weight_of_node(node.right_son) + 1)
        else:
            result = float(weight_of_node(node.left_son) + weight_of_node(node.right_son))
    return result


def weight_of_array(array):
    result = 0
    for i in range(len(array)):
        if array[i].type > 0:
            result += weight_of_node(array[i])
    return float(result)


def balance(u):
    result = Node(None, None)
    if len(u) == 0:
        return None
    if len(u) == 1:
        return u[0]
    weight_of_u = weight_of_array(u)
    if weight_of_u > 0:
        summa = 0
        u1 = []
        u2 = []
        for i in range(len(u)):
            if summa + weight_of_node(u[i]) < weight_of_u / 2:
                u1.append(u[i])
            else:
                u2.append(u[i])
                summa += weight_of_node(u[i])
        if len(u1) != 0:
            result.type = u1[len(u1) - 1].type
            result.data = u1[len(u1) - 1].data
            result.trap_num = u1[len(u1) - 1].trap_num
            u1.remove(u1[len(u1) - 1])
            result.left_son = balance(u1)

        result.right_son = u2[1]
        result.right_son.left_son = u2[0]
        u2.remove(u2[0])
        u2.remove(u2[0])
        result.right_son.right_son = balance(u2)
    else:
        middle = len(u) / 2
        u1 = []
        u2 = []
        for i in range(middle):
            u1.append(u[i])
        for i in range(middle + 1, len(u)):
            u2.append(u[i])
        result.type = u[middle].type
        result.data = u[middle].data
        result.trap_num = u[middle].trap_num
        result.left_son = balance(u1)
        result.right_son = balance(u2)
    return result


def trapezium_method(v_inside, e_inside, vertices):
    n = len(v_inside)
    tree = Node(Node.LEAF_NODE, None)

    if n <= 0:
        tree.trap_num = numbers[tr_num[0]]
        tr_num[0] += 1
        return tree

    v_inside_bottom = []
    v_inside_top = []

    e_inside_bottom = []
    e_inside_top = []

    u_bottom = []
    u_top = []

    median = v_inside[n / 2 - 1]

    bottom_limits = [v_inside[0].y, median.y]
    top_limits = [median.y, v_inside[len(v_inside) - 1].y]

    for e in e_inside:
        if bottom_limits[0] < e.start.y < bottom_limits[1]:
            if e.start not in v_inside_bottom:
                v_inside_bottom.append(e.start)
            if e not in e_inside_bottom:
                e_inside_bottom.append(e)
        if bottom_limits[0] < e.end.y < bottom_limits[1]:
            if e.end not in v_inside_bottom:
                v_inside_bottom.append(e.end)
            if e not in e_inside_bottom:
                e_inside_bottom.append(e)

        if crosses(e, bottom_limits[0], bottom_limits[1]):
            u_bottom.append(trapezium_method(v_inside_bottom, e_inside_bottom, vertices))
            bottom_tree = Node(Node.EDGE_NODE, e)
            u_bottom.append(bottom_tree)
            v_inside_bottom = []
            e_inside_bottom = []

        if top_limits[0] < e.start.y < top_limits[1]:
            if e.start not in v_inside_top:
                v_inside_top.append(e.start)
            if e not in v_inside_top:
                e_inside_top.append(e)
        if top_limits[0] < e.end.y < top_limits[1]:
            if e.end not in v_inside_bottom:
                v_inside_top.append(e.end)
            if e not in e_inside_bottom:
                e_inside_top.append(e)

        if crosses(e, top_limits[0], top_limits[1]):
            u_top.append(trapezium_method(v_inside_top, e_inside_top, vertices))
            top_tree = Node(Node.EDGE_NODE, e)
            u_top.append(top_tree)
            v_inside_top = []
            e_inside_top = []

    u_bottom.append(trapezium_method(v_inside_bottom, e_inside_bottom, vertices))
    u_top.append(trapezium_method(v_inside_top, e_inside_top, vertices))

    tree.type = Node.VERTEX_NODE
    tree.data = median
    tree.left_son = balance(u_bottom)
    tree.right_son = balance(u_top)

    return tree


def on_the_right(edge, point):
    start_x = edge.start.x - point.x
    start_y = edge.start.y - point.y
    end_x = edge.end.x - point.x
    end_y = edge.end.y - point.y

    if start_y * end_y > 0:
        return 1
    sign = numpy.sign(start_x * end_y - start_y * end_x)
    if sign == 0:
        if start_x * end_x <= 0:
            return 0
        return 1
    if start_y < 0:
        return -sign
    if end_y < 0:
        return sign
    return 1


def search(tree, point_to_locate):
    result = tree
    while result.type != Node.LEAF_NODE:
        if result.type == Node.VERTEX_NODE:
            if point_to_locate.y < result.data.y:
                result = result.left_son
            else:
                result = result.right_son
        else:
            if on_the_right(result.data, point_to_locate):
                result = result.left_son
            else:
                result = result.right_son
    return result.trap_num


def main():
    vertices = read_points("vertices.txt")
    edges = read_edges("edges.txt", vertices)

    point_to_locate = Point(5, 3, -1)
    tree = trapezium_method(vertices, edges, vertices)
    print(tree)
    print(search(tree, point_to_locate))


numbers = range(1, 100, 1)
tr_num = [0]
main()
