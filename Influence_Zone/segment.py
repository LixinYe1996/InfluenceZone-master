from Influence_Zone.data import Point, Segment, Line


class segment:
    # 分割
    def generate(points):
        segments = []
        for point in points:
            segments.extend(compute(point))
        return segments

    def mid_point(segment):
        x = (segment.spoint.x + segment.epoint.x) / 2.0
        y = (segment.spoint.y + segment.epoint.y) / 2.0
        return Point(-1, x, y)


def compute(points):
    index = 0
    segment = []
    while index < len(points) - 1:
        segment.append(Segment(points[index], points[index + 1]))
        index = index + 1
    return segment
