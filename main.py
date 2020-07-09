from Region_tree import RegionTree, Point, Rect, sequential_query
import time
from Influence_Zone.data import Point, Segment, Line
import matplotlib.pyplot as plt
from Influence_Zone.Intersection import intersection
import numpy as np
from Influence_Zone.Influence_Zone import dist, Influence_zone
import random


def construct_r_tree(data_points):
    # 批量初始化
    R_tree = RegionTree()
    temp_counter = 0
    # print("\033[H\033[J")
    # print("build R-Tree:\n0.0%\n", end="\r")
    for i in range(len(data_points)):
        if temp_counter >= len(data_points) / 1000:
            # print("\033[H\033[J")
            # print("build R-Tree:\n{:.1f}%\n".format(100 * i / len(data_points)), end="\r")
            temp_counter = temp_counter % (len(data_points) / 1000)
        R_tree.insert_point(data_points[i], cur_node=R_tree.root)
        temp_counter += 1

    return R_tree


def draw_scatter(Obeject_set, bisector, bound, intersect, segments, zone):
    """
    绘制点和垂直平分线
    :param Obeject_set: 点集
    :param bisector: 垂直平分线集
    :param bound: 边界集
    :return:
    """
    x1 = []
    y1 = []
    id = []
    for i in range(len(Obeject_set)):
        x1.append(Obeject_set[i].x)
        y1.append(Obeject_set[i].y)
        id.append(Obeject_set[i].id)
    print(x1)
    print(y1)
    #
    fig = plt.figure(figsize=(6, 6))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.scatter(x1, y1, c='k', marker='.')
    plt.xlim(0 - 0.1, bound + 0.1)
    plt.ylim(0 - 0.1, bound + 0.1)
    #
    for i in range(len(intersect)):
        x2 = []
        y2 = []
        for j in range(len(intersect[i])):
            # print(intersect[i][j].x,intersect[i][j].y)
            x2.append(intersect[i][j].x)
            y2.append(intersect[i][j].y)
        ax1.scatter(x2, y2, c='b', marker='.')

    for i in range(len(segments)):
        plt.plot([segments[i].spoint.x, segments[i].epoint.x], [segments[i].spoint.y, segments[i].epoint.y])

    for i in range(len(zone)):
        plt.plot([zone[i].spoint.x, zone[i].epoint.x], [zone[i].spoint.y, zone[i].epoint.y], color="red")

    for i in range(len(id)):
        ax1.text(x1[i], y1[i], id[i])
    plt.show()


def count_intersection(segment, bisector):
    count = 0
    for line in bisector:
        if intersection.line_segment(line, segment):
            count = count + 1
    return count


def draw_points(Obeject_set):
    x1 = []
    y1 = []
    id = []
    for i in range(len(Obeject_set)):
        x1.append(Obeject_set[i].x)
        y1.append(Obeject_set[i].y)
        id.append(Obeject_set[i].id)
    print(x1)
    print(y1)
    fig = plt.figure(figsize=(6, 6))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.scatter(x1, y1, c='k', marker='.')
    plt.xlim(0 - 0.1, bound + 0.1)
    plt.ylim(0 - 0.1, bound + 0.1)
    for i in range(len(id)):
        ax1.text(x1[i], y1[i], id[i])

    plt.show()


if __name__ == '__main__':
    # query_point=Point(0,8.0,4.0)
    # Object_set = [Point(1, 8.5, 6.0),
    #                Point(2, 4.5, 3.0),
    #                Point(3, 3.9, 5.8),
    #                Point(4,2.5,9.0),
    #                Point(5, 0, 9.9),
    #                Point(6, 9, 2)
    #                ]
    bound = 100
    point_num = 100000
    Object_set = []
    for i in range(point_num):
        x = random.uniform(0, bound)
        y = random.uniform(0, bound)
        Object_set.append(Point(i + 1, x, y))

    query_point = Point(0, 50, 50)
    Object_set.append(query_point)
    k = 16

    R_tree = construct_r_tree(Object_set)
    # R_tree.print_tree()

    import datetime

    start = datetime.datetime.now()
    InfZone = Influence_zone()
    InfZone.compute(query_point, R_tree.root, k, bound, Object_set)
    rknn = InfZone.rknn()

    end = datetime.datetime.now()
    print("用时:", (end - start))
    print("RKNN")
    for p in rknn:
        print(p)
