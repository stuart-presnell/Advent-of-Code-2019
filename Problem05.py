from operator import add, mul
from itertools import zip_longest

def list_from_file(filename, sep='\n'):
    """Return the content of the named file as a list of strings"""
    f = open(filename)
    file_content = f.read()
    f.close()
    return file_content.split(sep)

def modify_list(list, location, value):
    return list[:location] + [value] + list[(location+1):]

def int_to_list_of_digits(n):
    return [int(x) for x in str(n)]


# def process(intcode, pointer, op):
#         [loca,locb,locc] = intcode[pointer+1:pointer+4]
#         va = intcode[loca]
#         vb = intcode[locb]
#         val = op(va,vb)
#         new_list = modify_list(intcode, locc, val)
#         return (new_list, pointer+4)

def interpret_opcode(raw):
    """Given a number, interpret it as an opcode plus a list of parameter modes:
    e.g. ABCDE = opcode DE, plus parameter modes [C, B, A]"""
    L = int_to_list_of_digits(raw)
    u = L.pop()
    try:
        t = L.pop()
    except IndexError:
        t = 0
    opcode = 10*t + u
    L.reverse()
    return (opcode, L)


def step(intcode, pointer):
    """Given an intcode program and a pointer to a position, 
    compute one step of the program and either exit or 
    return an updated intcode program and pointer position"""
    raw_opcode = intcode[pointer]
    (opcode, modes) = interpret_opcode(raw_opcode)

    if opcode == 99:    # '99' is the termination code
        return (intcode, -1)  # Using pointer=-1 to signal termination
    elif opcode == 1:
        return step_add(intcode, pointer, modes)
    elif opcode == 2:
        return step_mult(intcode, pointer, modes)
    elif opcode == 3:
        return step_input(intcode, pointer, modes)
    elif opcode == 4:
        return step_output(intcode, pointer, modes)
    else:
        raise ValueError("opcode is not 1, 2, 3, 4, or 99")

def lookup_val(intcode, param, mode):
    if mode == 0:   # "position mode causes the parameter to be interpreted as a position - if the parameter is 50, its value is the value stored at address 50 in memory."
        return intcode[param]
    elif mode == 1: # "In immediate mode, a parameter is interpreted as a value - if the parameter is 50, its value is simply 50."
        return param
    else:
        raise ValueError("I only understand Position mode (0) and Immediate mode (1)")

# def convert_values(L, modes):
#     args = list(zip_longest(L, modes, fillvalue=0)) 
#         # list of pairs [(param_i, mode_i)], with default mode = 0
#     inputs = [lookup_val(intcode, p, m) for (p,m) in args]
#         # each param has now been interpreted according to its mode

def read_values(intcode, position, x, modes):
    """Given a position in the intcode program, a list of parameter modes, and a number x of values to lookup,
    return a list of values"""
    L = intcode[position:position+x]    # The x elements of intcode starting at 'position'
    elements_and_modes = list(zip_longest(L, modes, fillvalue=0))  # list of pairs [(elt_i, mode_i)], with default mode = 0
    return [lookup_val(intcode, e, m) for (e,m) in elements_and_modes]

def step_add(intcode, pointer, modes):
    """Read the values according to modes, then return the modified program & pointer"""
    inputs = read_values(intcode, pointer+1, 2, modes)
    write_location = intcode[pointer+3]
    v = inputs[0] + inputs[1]
    new_list = modify_list(intcode, write_location, v)
    return (new_list, pointer+4)

def step_mult(intcode, pointer, modes):
    """Read the values according to modes, then return the modified program & pointer"""
    """Read the values according to modes, then return the modified program & pointer"""
    inputs = read_values(intcode, pointer+1, 2, modes)
    write_location = intcode[pointer+3]
    v = inputs[0] * inputs[1]
    new_list = modify_list(intcode, write_location, v)
    return (new_list, pointer+4)

def step_input(intcode, pointer, modes):
    """Read input from the user, write to location"""
    write_location = intcode[pointer+1]
    val = int(input("Input: "))
    new_list = modify_list(intcode, write_location, val)
    return (new_list, pointer+2)

def step_output(intcode, pointer, modes):
    """Print output from specified location"""
    val = read_values(intcode, pointer+1, 1, modes)[0]
    # location = intcode[pointer+1]
    # val = intcode[location]
    print("Output: " + str(val))
    return (intcode, pointer+2)

def run(intcode):
    pointer = 0
    while pointer > -1:
        (intcode, pointer) = step(intcode, pointer)
    return intcode

def verbose_run(prog):
    print("Initial program:")
    print(prog)
    final_state = run(prog)
    print("Final program:")
    print(final_state)

####################################
# Testing the program on the provided test inputs:

# testprog0 = [
#     1002,4,3,4,
#     33
# ]

# testprog1 = [
#     1101,100,-1,4,
#     0
# ]

# testprog3 = [
#     3,0,
#     99
# ]

# testprog4 = [
#     4,2,
#     99
# ]

# for p in [testprog0, testprog1, testprog3, testprog4]: 
#     verbose_run(p)
#     print()


####################################
# Problem 5a:

# prob5a_text = list_from_file("Prob5-input.txt", sep=",")
# prob5a_code = [int(x) for x in prob5a_text]
# run(prob5a_code)
# Answer: 4601506


####################################
# Problem 5b:
# verb = 12
# noun = 2

# prob2b_base = [int(x) for x in list_from_file("Prob2-intcode.txt", sep=",")]

# def input_verb_noun(prog, noun, verb):
#     """Given a verb and a noun, input them into positions 1 and 2 of prog"""
#     prog_v1 = modify_list(prog, 1, noun)
#     prog_v2 = modify_list(prog_v1, 2, verb)
#     return prog_v2

# def run_AGC(noun, verb):
#     """Run the Apollo Guidance Computer (with fixed prob2b_base)
#     using specified verb and noun,
#     return the final value of address 0"""
#     prog = input_verb_noun(prob2b_base, noun, verb)
#     output = run(prog)
#     return output[0]

# print(run_AGC(0,0))

# print(run_AGC(12,2))

# def find_target_value(target):
#     for noun in range(100):
#         for verb in range(100):
#             if run_AGC(noun, verb) == target:
#                 return (100 * noun + verb)

# print(find_target_value(19690720))
# Answer: 2552

# Checking this answer:
# print(run_AGC(25,52))


# Investigating this further:
# prog0 = input_verb_noun(prob2b_base, 12, 2)

# prog1 = step(prog0,0)[0]
# prog2 = step(prog1,4)[0]

# print(prog0[:20])
# print(prog1[:20])
# print(prog2[:20])