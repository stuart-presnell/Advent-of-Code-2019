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

def children_dict(L: List[Body]) -> Dict[Body,List[Body]]:
    D = {}
    kvs = [xy.split(')') for xy in L] # [['COM', 'B'], ... , ['K', 'L']]
    for [sun, planet] in kvs:
        if sun in D:
            D[sun].append(planet)
        else:
            D[sun] = [planet]
    return D

def calculate_orbits(D: Dict[Body,List[Body]]) -> Dict[Body,int]:
    """Given a dictionary of Bodies and their children: {'COM': ['B'], 'B': ['C', 'G'], 'C': ['D'], 'D': ['E', 'I'], 'E': ['F', 'J'], 'G': ['H'], 'J': ['K'], 'K': ['L']}
    return a dictionary of Bodies and their orbits"""
    orbits = {'COM': 0}
    # print("Orbits known: " + str(orbits))
    objects_to_process = [(planet, 'COM') for planet in D['COM']]
    # print("Objects remaining to be processed: " + str(objects_to_process))
    while objects_to_process:
        (planet, sun) = objects_to_process[0]
        # print("Current planet: " + planet + "; Sun: " + sun)
        orbits[planet] = 1 + orbits[sun] # The number of indirect orbits of an object is 1 + the number of indirect orbits of its parent
        # print("Orbits for " + planet + " = " + str(orbits[planet]))
        if planet in D:
            new_objects = [(moon, planet) for moon in D[planet]]
            # print(new_objects)
            objects_to_process.extend(new_objects)
            # print("New list of objects to be processed: " + str(objects_to_process))
        objects_to_process.remove((planet,sun))
    return orbits
    
def total_orbits(L: List[Body]) -> int:
    C = children_dict(L)
    O = calculate_orbits(C)
    return sum(list(O.values()))




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







####################################
# Running the code on the main data:
####################################

# prob6b_input: List[str]         = list_from_file('Prob6-input.txt')
# print(total_orbits(prob6b_input))

# Answer: 


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
# test_parents = find_parents(test_orbits) # [('I', ['D']), ('J', ['E']), ('F', ['E']), ('L', ['K']), ('COM', []), ('G', ['B']), ('D', ['C']), ('H', ['G']), ('C', ['B']), ('E', ['D']), ('B', ['COM']), ('K', ['J'])]


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
