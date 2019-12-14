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
    compute one step of the program based on the opcode at that pointer position 
    and either exit or return an updated intcode program and pointer position"""
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
    elif opcode == 5:
        return step_jump_if_true(intcode, pointer, modes)
    elif opcode == 6:
        return step_jump_if_false(intcode, pointer, modes)
    elif opcode == 7:
        return step_less_than(intcode, pointer, modes)
    elif opcode == 8:
        return step_equal(intcode, pointer, modes)
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

#######################################################################
# Implementing the opcodes:
#######################################################################

def step_add(intcode, pointer, modes):  # opcode 1
    """Read the values according to modes, then return the modified program & pointer"""
    inputs = read_values(intcode, pointer+1, 2, modes)  # Read 2 inputs
    write_location = intcode[pointer+3]
    v = inputs[0] + inputs[1]
    new_list = modify_list(intcode, write_location, v)
    return (new_list, pointer+4)

def step_mult(intcode, pointer, modes):  # opcode 2
    """Read the values according to modes, then return the modified program & pointer"""
    inputs = read_values(intcode, pointer+1, 2, modes)  # Read 2 inputs
    write_location = intcode[pointer+3]
    v = inputs[0] * inputs[1]
    new_list = modify_list(intcode, write_location, v)
    return (new_list, pointer+4)

def step_input(intcode, pointer, modes):  # opcode 3
    """Read input from the user, write to location"""
    write_location = intcode[pointer+1]
    val = int(input("Input: "))
    new_list = modify_list(intcode, write_location, val)
    return (new_list, pointer+2)

def step_output(intcode, pointer, modes):  # opcode 4
    """Print output from specified location"""
    val = read_values(intcode, pointer+1, 1, modes)[0]  # Read 1 input
    print("Output: " + str(val))
    return (intcode, pointer+2)

def step_jump_if_true(intcode, pointer, modes):  # opcode 5
    """if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing."""
    inputs = read_values(intcode, pointer+1, 2, modes)  # Read 2 inputs
    if inputs[0] == 0:
        return (intcode, pointer+3)
    else:
        return (intcode, inputs[1])

def step_jump_if_false(intcode, pointer, modes):  # opcode 6
    """if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing."""
    inputs = read_values(intcode, pointer+1, 2, modes)  # Read 2 inputs
    if inputs[0] == 0:
        return (intcode, inputs[1])
    else:
        return (intcode, pointer+3)

def step_less_than(intcode, pointer, modes):  # opcode 7
    """if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0."""
    inputs = read_values(intcode, pointer+1, 2, modes)  # Read 2 inputs
    write_location = intcode[pointer+3] # and a write location
    if inputs[0] < inputs[1]:
        val = 1
    else:
        val = 0
    new_list = modify_list(intcode, write_location, val)
    return (new_list, pointer+4)

def step_equal(intcode, pointer, modes):  # opcode 8
    """if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0."""
    inputs = read_values(intcode, pointer+1, 2, modes)  # Read 2 inputs
    write_location = intcode[pointer+3] # and a write location
    if inputs[0] == inputs[1]:
        val = 1
    else:
        val = 0
    new_list = modify_list(intcode, write_location, val)
    return (new_list, pointer+4)


######################################################################

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


# for p in [testprog5b_7]:
#     run(p)
#     print()


####################################
# Problem 5a:

# prob5a_text = list_from_file("Prob5-input.txt", sep=",")
# prob5a_code = [int(x) for x in prob5a_text]
# run(prob5a_code)
# Answer: 4601506


####################################
# Problem 5b:
# prob5b_text = list_from_file("Prob5-input.txt", sep=",")
# prob5b_code = [int(x) for x in prob5b_text]
# run(prob5b_code)
# # Answer: 5525561
