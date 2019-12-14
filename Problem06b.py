from itertools import chain
from typing import List, Dict

Body = str

def list_from_file(filename:str, sep='\n') -> List[str]:
    """Return the content of the named file as a list of strings"""
    f = open(filename)
    file_content = f.read()
    f.close()
    return file_content.split(sep)

def parent_dict(L: List[Body]) -> Dict[Body,Body]:
    """Given a list of strings ['COM)B', 'B)C', 'C)D', ...]
    return a dictionary {'B': 'COM', 'C': 'B', 'D': 'C', ...}
    listing for each object the thing it orbits around (i.e. its 'parent')"""
    kvs = [xy.split(')') for xy in L]  # [['COM', 'B'], ... , ['K', 'L']]
    return {planet:sun for [sun,planet] in kvs}

def find_chain(P: Dict[Body,Body], start_obj: Body) -> List[Body]:
    """Given a dictionary showing the parent of each body, and a particular body,
    return the sequence of bodies from start_obj to COM"""
    ch = [start_obj]
    while ch[-1] != 'COM':
        ch.append(P[ch[-1]])
    return ch

def intersect_chains(c1, c2):
    for x in c1:
        if x in c2:
            i1 = c1.index(x)
            i2 = c2.index(x)
            return (c1[:i1+1], c2[:i2+1])

def number_of_transfers(L: List[Body], start_obj: Body, end_obj: Body) -> int:
    P = parent_dict(L)
    c1 = find_chain(P, start_obj)
    c2 = find_chain(P, end_obj)
    (route1, route2) = intersect_chains(c1, c2)
    return len(route1) + len(route2) - 4


####################################
# Testing the code:
####################################

test_input: List[Body] = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN""".split('\n')

# P = parent_dict(test_input)
# Cy = find_chain(P, 'YOU')
# Cs = find_chain(P, 'SAN')
# print(Cy)
# print(Cs)
# print(intersect_chains(Cy,Cs))

# print(number_of_transfers(test_input, 'SAN', 'YOU'))

####################################
# Running the code on the main data:
####################################

prob6b_input: List[str]         = list_from_file('Prob6-input.txt')
print(number_of_transfers(prob6b_input, 'YOU', 'SAN'))

# Answer: 322


####################################
####################################
# Unused earlier draft code:
####################################

# def find_all_objects(list_of_orbits):
#     """Given a list of pairs [['COM', 'B'], ... , ['K', 'L']]
#     return a list of unique objects"""
#     flatlist = list(chain.from_iterable(list_of_orbits))
#     return list(set(flatlist)) # Just each element once

# def parent(object, list_of_orbits):
#     return [x for [x,y] in list_of_orbits if y==object]

# def find_parents(list_of_orbits):
#     """Given a list of orbits, return the list of (object, parent of object)"""
#     objects = find_all_objects(list_of_orbits)
#     return [(ob, parent(ob, list_of_orbits))   for ob in objects]

# test_orbits: List[List[str]] = [xy.split(')') for xy in test_input] # [['COM', 'B'], ... , ['K', 'L']]
# test_objects: List[str] = find_all_objects(test_orbits) # ['E', 'F', 'J', 'B', 'D', 'L', 'G', 'C', 'I', 'K', 'H', 'COM']
# test_parents = find_parents(test_orbits) 
# # [('I', ['D']), ('J', ['E']), ('F', ['E']), ('L', ['K']), ('COM', []), ('G', ['B']), ('D', ['C']), ('H', ['G']), ('C', ['B']), ('E', ['D']), ('B', ['COM']), ('K', ['J'])]


####################################
# Test data for Problem 6a
####################################

# test_input: List[Body] = """COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L""".split('\n')

# P = parent_dict(test_input)
# C = children_dict(test_input)
# O = calculate_orbits(C)
# T = list(O.values())
# print(O)
# print(T)
# print(total_orbits(test_input))
####################################



