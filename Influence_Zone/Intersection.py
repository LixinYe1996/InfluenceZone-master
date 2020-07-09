from Influence_Zone.data import Point, Segment, Line
from Influence_Zone.Functions import dist


class intersection:
    def generate(self, lines, tbisector, bound, query_point, eindex, points):
        """
        根据新增垂直平分线 增量更新交点
        :param lines: 垂直平分线
        :param tbisector: 新增垂直平分线
        :param bound: 边界
        :param query_point:查询点
        :param eindex: 修建影响区的点
        :param intersect: 当前交点
        :return:
        """
        point = []
        # 最终新增有效的交点
        cleaned = []
        if len(lines) == 0:
            point.extend(compute_bound(tbisector[0], bound))
            cleaned.extend(sort(remove_outside_bound(point, bound)))
        else:
            for line in lines:
                point.append(compute(line, tbisector[0]))
            point.extend(compute_bound(tbisector[0], bound))
            cleaned.extend(sort(remove_outside_bound(point, bound)))
        e = eindex[-1]
        # 使用新增的垂直平分线对之前的交点进行更新
        for p in points:
            if abs(dist(p[0], e) - dist(p[0], query_point)) < 0.00001:
                continue
            if dist(p[0], e) < dist(p[0], query_point):
                p[1] = p[1] + 1
        # 使用之前的垂直平分线计算新增交点的count
        for p in cleaned:
            count = 0
            for e in eindex:
                # 处理计算误差
                if abs(dist(p, e) - dist(p, query_point)) < 0.00001:
                    continue
                if dist(p, e) < dist(p, query_point):
                    count = count + 1
            points.append([p, count])

        return points

    def segment(segment_1, segment_2):
        orientation_1 = calucation_orientation(segment_1.spoint, segment_1.epoint, segment_2.spoint)
        orientation_2 = calucation_orientation(segment_1.spoint, segment_1.epoint, segment_2.epoint)
        orientation_3 = calucation_orientation(segment_2.spoint, segment_2.epoint, segment_1.spoint)
        orientation_4 = calucation_orientation(segment_2.spoint, segment_2.epoint, segment_1.epoint)
        return orientation_1 != orientation_2 and orientation_3 != orientation_4

    def line_segment(line, segment):
        if (segment.epoint.y - segment.spoint.y + line.m * (segment.spoint.x - segment.epoint.x)) == 0:
            t = float('inf')
        else:
            t = (line.c - segment.spoint.y + line.m * segment.spoint.x) / (
                        segment.epoint.y - segment.spoint.y + line.m * (segment.spoint.x - segment.epoint.x))
        return t >= 0.0 and t <= 1.0


def calucation_orientation(point_1, point_2, point_3):
    val = (point_2.y - point_1.y) * (point_3.x - point_2.x) - (point_2.x - point_1.x) * (point_3.y - point_2.y)
    if val == 0.0:
        return 0
    if val > 0.0:
        return 1
    if val < 0.0:
        return 2


def compute(line_1, line_2):
    x = calculate_x(line_1, line_2)
    y = (line_1.m * x) + line_1.c
    return Point(-1, x, y)


def calculate_x(line_1, line_2):
    # print(line_2.c,line_2.c,line_1.m,line_2.m)
    if line_1.m == line_2.m:
        return float("inf")
    else:
        return (line_2.c - line_1.c) / (line_1.m - line_2.m)


def compute_bound(line, bound):
    points = []
    point = Point(-1, 0.0, line.c)
    points.append(point)

    point = Point(-1, bound, (line.m * bound) + line.c)
    points.append(point)

    if line.m == 0:
        point = Point(-1, float("inf"), 0.0)
    else:
        point = Point(-1, -line.c / line.m, 0.0)
    points.append(point)

    if line.m == 0:
        point = Point(-1, float("inf"), bound)
    else:
        point = Point(-1, (bound - line.c) / line.m, bound)
    points.append(point)
    return points


def remove_outside_bound(points, bound):
    cleaned = []
    for point in points:
        if point.x >= 0.0 and point.x <= bound and point.y >= 0 and point.y <= bound:
            cleaned.append(point)
    return cleaned


def sort(points):
    sortedpoints = points
    sortedpoints = sorted(sortedpoints, key=lambda p: p.x)
    sortedpoints = sorted(sortedpoints, key=lambda p: p.y)
    # for i in  sortedpoints:
    #     print(i)
    return sortedpoints
