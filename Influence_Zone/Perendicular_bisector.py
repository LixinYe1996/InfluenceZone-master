from Influence_Zone.data import Point, Segment, Line


class perendicular_bisector:
    # 垂直平分线
    def generate(self, query_point, interest_points):
        lines = []
        for point in interest_points:
            lines.append(compute(query_point, point))
        return lines


def compute(point_1, point_2):
    # 斜率
    if calculate_slope(point_1, point_2) == 0:
        m = float("inf")
        c = (point_1.x + point_2.x) / 2
    else:
        m = -1.0 / calculate_slope(point_1, point_2)
        c = calculate_c(m, calculate_mid(point_1, point_2))
    # y=mx+c

    return Line(m, c)


def calculate_slope(point_1, point_2):
    if point_2.x == point_1.x:
        return float("inf")
    return (point_2.y - point_1.y) / (point_2.x - point_1.x)


def calculate_mid(point_1, point_2):
    return Point(-1, (point_1.x + point_2.x) / 2.0, (point_1.y + point_2.y) / 2.0)


def calculate_c(slope, mid_point):
    return (mid_point.y - mid_point.x * slope)
