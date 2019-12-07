from operator import add, mul

def list_from_file(filename, sep='\n'):
    """Return the content of the named file as a list of strings"""
    f = open(filename)
    file_content = f.read()
    f.close()
    return file_content.split(sep)

def modify_list(list, location, value):
    return list[:location] + [value] + list[(location+1):]

def process(intcode, pointer, op):
        [loca,locb,locc] = intcode[pointer+1:pointer+4]
        va = intcode[loca]
        vb = intcode[locb]
        val = op(va,vb)
        new_list = modify_list(intcode, locc, val)
        return (new_list, pointer+4)

def step(intcode, pointer):
    """Given an intcode program and a pointer to a position, 
    compute one step of the program and either exit or 
    return an updated intcode program and pointer position"""
    # if pointer < 0 or pointer > len(intcode)-1:
    #     raise IndexError("pointer must be within range of intcode program")
    opcode = intcode[pointer]
    if opcode == 99:    # '99' is the termination code
        return (intcode, -1)  # Using pointer=-1 to signal termination
    elif opcode == 1:
        return process(intcode, pointer, add)
    elif opcode == 2:
        return process(intcode, pointer, mul)
    else:
        raise ValueError("opcode is not 1, 2, or 99")


def run(intcode):
    pointer = 0
    while pointer > -1:
        (intcode, pointer) = step(intcode, pointer)
    return intcode

def verbose_run(prog):
    print("Initial program:")
    print(prog)
    print("Final output:")
    print(run(prog))

####################################
# Testing the program on the provided test inputs:

# testprog0 = [
#     1,9,10,3,
#     2,3,11,0,
#     99,
#     30,40,50
#     ]

# testprog1 = [1,0,0,0,99]
# testprog2 = [2,3,0,3,99]
# testprog3 = [2,4,4,5,99,0]
# testprog4 = [1,1,1,4,99,5,6,0,99]

# for p in [testprog1, testprog2, testprog3, testprog4]: 
#     verbose_run(p)
#     print()


####################################
# Problem 2a:

# prob2a_text = list_from_file("Prob2-intcode-corrected.txt", sep=",")
# prob2a_code = [int(x) for x in prob2a_text]
# verbose_run(prob2a_code)
# Answer: 9706670


####################################
# Problem 2b:
# verb = 12
# noun = 2

prob2b_base = [int(x) for x in list_from_file("Prob2-intcode.txt", sep=",")]

def input_verb_noun(prog, noun, verb):
    """Given a verb and a noun, input them into positions 1 and 2 of prog"""
    prog_v1 = modify_list(prog, 1, noun)
    prog_v2 = modify_list(prog_v1, 2, verb)
    return prog_v2

def run_AGC(noun, verb):
    """Run the Apollo Guidance Computer (with fixed prob2b_base)
    using specified verb and noun,
    return the final value of address 0"""
    prog = input_verb_noun(prob2b_base, noun, verb)
    output = run(prog)
    return output[0]

# print(run_AGC(0,0))

# print(run_AGC(12,2))

def find_target_value(target):
    for noun in range(100):
        for verb in range(100):
            if run_AGC(noun, verb) == target:
                return (100 * noun + verb)

print(find_target_value(19690720))
# Answer: 2552

# Checking this answer:
print(run_AGC(25,52))


# Investigating this further:
# prog0 = input_verb_noun(prob2b_base, 12, 2)

# prog1 = step(prog0,0)[0]
# prog2 = step(prog1,4)[0]

# print(prog0[:20])
# print(prog1[:20])
# print(prog2[:20])