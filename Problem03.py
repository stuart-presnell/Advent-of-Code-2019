# from operator import add, mul

def list_from_file(filename, sep='\n'):
    """Return the content of the named file as a list of strings"""
    f = open(filename)
    file_content = f.read()
    f.close()
    return file_content.split(sep)

# def modify_list(list, location, value):
#     return list[:location] + [value] + list[(location+1):]

def process_wire(wire_string):
    """Turn the string 'R999,...' into a list of tuples [('R', 999), ...] """
    wire_list = wire_string.split(',')
    wire = [(x[0], int(x[1:])) for x in wire_list]
    return wire

def points_included(wire):
    """Record the set of points included in the trail of the given wire"""
    points = []
    pos = (0,0)
    for seg in wire:
        pts = follow_segment(seg, pos)
        pos = pts[-1]
        points.extend(pts)
    return points

def follow_segment(seg, start):
    """Given a segment, like ('R', 5), and a starting point like (3,10),
    return a list of the points added to the trail by following that segment,
    and the point reached at the end of the segment."""
    pts = []
    (x0,y0) = start
    (dir, dist) = seg
    if   dir == 'R':
        return [(x0 + x + 1, y0) for x in range(dist)]
    elif dir == 'L':
        return [(x0 - x - 1, y0) for x in range(dist)]
    elif dir == 'U':
        return [(x0, y0 + y + 1) for y in range(dist)]
    elif dir == 'D':
        return [(x0, y0 - y - 1) for y in range(dist)]
    else:
        raise ValueError(dir + " is not a valid direction")

def collisions(wire1, wire2):
    """Given two wires, return the list of points common to both paths"""
    return list(set(wire1) & set(wire2))

def closest_by_md(list_of_points):
    list_of_dist = [ abs(x)+abs(y) for (x,y) in list_of_points]
    return min(list_of_dist)

def find_nearest_collision(wire_string1, wire_string2):
    ptsA = points_included(process_wire(wire_string1))
    ptsB = points_included(process_wire(wire_string2))
    coll = collisions(ptsA, ptsB)
    return closest_by_md(coll)


# # Testing the proved examples:
# test_wire_1A = "R8,U5,L5,D3"
# test_wire_1B = "U7,R6,D4,L4"

# test_wire_2A = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
# test_wire_2B = "U62,R66,U55,R34,D71,R55,D58,R83"

# test_wire_3A = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
# test_wire_3B = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"

# print( find_nearest_collision(test_wire_1A, test_wire_1B) )
# print( find_nearest_collision(test_wire_2A, test_wire_2B) )
# print( find_nearest_collision(test_wire_3A, test_wire_3B) )

[wireA,wireB] = list_from_file("Prob3-input.txt")

print( find_nearest_collision(wireA, wireB) )
# Answer: 1017