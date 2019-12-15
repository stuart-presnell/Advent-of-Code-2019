from itertools import zip_longest
from itertools import permutations
# from collections import deque       # May want to use a deque to implement the "world" as a queue

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


def step(intcode, pointer, world):
    """Given an intcode program and a pointer to a position, plus the state of the "world",
    compute one step of the program based on the opcode at that pointer position 
    and either exit or return an updated intcode program and pointer position.
    In all cases, return the state of the world as well."""
    raw_opcode = intcode[pointer]
    (opcode, modes) = interpret_opcode(raw_opcode)

    if opcode == 99:    # '99' is the termination code
        return (intcode, -1, world)  # Using pointer=-1 to signal termination
    elif opcode == 1:
        return step_add(intcode, pointer, modes, world)
    elif opcode == 2:
        return step_mult(intcode, pointer, modes, world)
    elif opcode == 3:
        return step_input(intcode, pointer, modes, world)
    elif opcode == 4:
        return step_output(intcode, pointer, modes, world)
    elif opcode == 5:
        return step_jump_if_true(intcode, pointer, modes, world)
    elif opcode == 6:
        return step_jump_if_false(intcode, pointer, modes, world)
    elif opcode == 7:
        return step_less_than(intcode, pointer, modes, world)
    elif opcode == 8:
        return step_equal(intcode, pointer, modes, world)
    else:
        raise ValueError("raw_opcode was " + str(raw_opcode) + " giving opcode " + str(opcode) + " which is not 1--8, or 99")

def lookup_val(intcode, param, mode):
    if mode == 0:   # "position mode causes the parameter to be interpreted as a position - if the parameter is 50, its value is the value stored at address 50 in memory."
        return intcode[param]
    elif mode == 1: # "In immediate mode, a parameter is interpreted as a value - if the parameter is 50, its value is simply 50."
        return param
    else:
        raise ValueError("I only understand Position mode (0) and Immediate mode (1)")


def read_values(intcode, position, x, modes):
    """Given a position in the intcode program, a list of parameter modes, and a number x of values to lookup,
    return a list of values"""
    L = intcode[position:position+x]    # The x elements of intcode starting at 'position'
    elements_and_modes = list(zip_longest(L, modes, fillvalue=0))  # list of pairs [(elt_i, mode_i)], with default mode = 0
    return [lookup_val(intcode, e, m) for (e,m) in elements_and_modes]

def fetch_input(world):
    """Given a world, either take the first value from it or ask user for input.
    Return the given value and the (possibly modified) world."""
    if world == []:
        val = int(input("Input: ")) # If the world is empty, ask the user
        new_world = world
    else:
        val = world[0]
        new_world = world[1:]
    return (val, new_world)

#######################################################################
# Implementing the opcodes:
#######################################################################

def step_add(intcode, pointer, modes, world):  # opcode 1
    """Read the values according to modes, then return the modified program & pointer"""
    inputs = read_values(intcode, pointer+1, 2, modes)  # Read 2 inputs
    write_location = intcode[pointer+3]
    v = inputs[0] + inputs[1]
    new_prog = modify_list(intcode, write_location, v)
    return (new_prog, pointer+4, world)

def step_mult(intcode, pointer, modes, world):  # opcode 2
    """Read the values according to modes, then return the modified program & pointer"""
    inputs = read_values(intcode, pointer+1, 2, modes)  # Read 2 inputs
    write_location = intcode[pointer+3]
    v = inputs[0] * inputs[1]
    new_prog = modify_list(intcode, write_location, v)
    return (new_prog, pointer+4, world)

def step_input(intcode, pointer, modes, world):  # opcode 3
    """Read input from the user, write to location"""
    write_location = intcode[pointer+1]
    (val, new_world) = fetch_input(world)
    new_prog = modify_list(intcode, write_location, val)
    # new_world = world       # ZEROTH DRAFT: leaving the world unchanged
    return (new_prog, pointer+2, new_world)

def step_output(intcode, pointer, modes, world):  # opcode 4
    """Print output from specified location"""
    val = read_values(intcode, pointer+1, 1, modes)[0]  # Read 1 input
    # print("Output: " + str(val))
    new_world = world + [val]      # FIRST DRAFT: append output to the end
    return (intcode, pointer+2, new_world)

def step_jump_if_true(intcode, pointer, modes, world):  # opcode 5
    """if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing."""
    inputs = read_values(intcode, pointer+1, 2, modes)  # Read 2 inputs
    if inputs[0] == 0:
        return (intcode, pointer+3, world)
    else:
        return (intcode, inputs[1], world)

def step_jump_if_false(intcode, pointer, modes, world):  # opcode 6
    """if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing."""
    inputs = read_values(intcode, pointer+1, 2, modes)  # Read 2 inputs
    if inputs[0] == 0:
        return (intcode, inputs[1], world)
    else:
        return (intcode, pointer+3, world)

def step_less_than(intcode, pointer, modes, world):  # opcode 7
    """if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0."""
    inputs = read_values(intcode, pointer+1, 2, modes)  # Read 2 inputs
    write_location = intcode[pointer+3] # and a write location
    if inputs[0] < inputs[1]:
        val = 1
    else:
        val = 0
    new_list = modify_list(intcode, write_location, val)
    return (new_list, pointer+4, world)

def step_equal(intcode, pointer, modes, world):  # opcode 8
    """if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0."""
    inputs = read_values(intcode, pointer+1, 2, modes)  # Read 2 inputs
    write_location = intcode[pointer+3] # and a write location
    if inputs[0] == inputs[1]:
        val = 1
    else:
        val = 0
    new_list = modify_list(intcode, write_location, val)
    return (new_list, pointer+4, world)


######################################################################

def run(prog, world=[]):
    pointer = 0
    while pointer > -1:
        (prog, pointer, world) = step(prog, pointer, world)
    return (prog, world)

def verbose_run(prog, world=[]):
    print("Initial world: " + str(world))
    print("Initial program:")
    print(prog)
    (final_state, final_world) = run(prog, world)
    print("Final program:")
    print(final_state)
    print("Final world: " + str(final_world))

######################################################################
def chain_amplifiers(program, phase_settings, initial_value=0):
    val = initial_value
    for phase in phase_settings:
        world = [phase, val]
        output = run(program, world)
        val = output[1][0]
        # print(val)
    return val




def find_max_output(program, settings_list=range(5), initial_value=0):
    max_output = 0
    for phase_settings in list(permutations(settings_list)):
        output = chain_amplifiers(program, phase_settings, 0)
        if output > max_output:
            max_output = output
    return max_output



######################################################################
# Main problem:
######################################################################

prob7a_raw_input = list_from_file("Prob7-input.txt", ',')
prob7a_input = [int(x) for x in prob7a_raw_input]
print(find_max_output(prob7a_input))
# Answer: 206580



######################################################################
# Testing on the given test data:
######################################################################
# phase_settings_1 = [4,3,2,1,0]
# phase_settings_2 = [0,1,2,3,4]
# phase_settings_3 = [1,0,4,3,2]
phase_settings_4 = [9,8,7,6,5]

# testprog7a_1 = [
#     3,15,       # Read input to {15}
#     3,16,       # Read input to {16}
#     1002,16,10,16, # Multiply {16} by 10, write to {16}
#     1,16,15,15, # Add {16} and {15}, write to {15}
#     4,15,       # Output {15}
#     99,0,0]     # x, y |-> (10*y + x)

# testprog7a_2 = [
#     3,23,
#     3,24,
#     1002,24,10,24,
#     1002,23,-1,23,
#     101,5,23,23,
#     1,24,23,23,
#     4,23,
#     99,0,0]

# testprog7a_3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

testprog7a_4 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

# # output = chain_amplifiers(testprog7a_1, phase_settings_1, 0)
# # output = chain_amplifiers(testprog7a_2, phase_settings_2, 0)
# # output = chain_amplifiers(testprog7a_3, phase_settings_3, 0)

# m1 = find_max_output(testprog7a_1)
# m2 = find_max_output(testprog7a_2)
# m3 = find_max_output(testprog7a_3)

# print(m3)

# print("Output from phase settings " + str(phase_settings_3) + " is: " + str(output))
######################################################################







####################################
# Problem 5a:

# prob5a_text = list_from_file("Prob5-input.txt", sep=",")
# prob5a_code = [int(x) for x in prob5a_text]
# run(prob5a_code)
# Answer: 4601506

####################################
# Test inputs from previous problems:

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

# testprog5b_1 = [
#     3,9,
#     8,9,10,9,
#     4,9,99,-1,8]  #Using position mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).

# testprog5b_2 = [
#     3,9,
#     7,9,10,9,
#     4,9,99,-1,8]  #Using position mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).

# testprog5b_3 = [
#     3,3,
#     1108,-1,8,3,
#     4,3,99]  #Using immediate mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).

# testprog5b_4 = [
#     3,3,
#     1107,-1,8,3,
#     4,3,99]  #Using immediate mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).

# testprog5b_5 = [
#     3,12,     # Store input in {12}
#     6,12,15,  # If input is zero, jump to instruction at {15}=9
#     1,13,14,13, # Else add 1 to content of {13}
#     4,13,99,-1,0,1,9] # take an input, then output 0 if the input was zero, or 1 if the input was non-zero:

# testprog5b_6 = [
#     3,3,     # Store input in {3}
#     1105,-1,9,  # If input is non-zero, jump to instruction at 9
#     1101,0,0,12, # Else write 0+0 to {12}
#     4,12,99,1] # take an input, then output 0 if the input was zero, or 1 if the input was non-zero:

# testprog5b_7 = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
# """The above example program uses an input instruction to ask for a single number. 
# The program will then output 999 if the input value is below 8, output 1000 if the input value is equal to 8, or output 1001 if the input value is greater than 8."""
