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



prob2text = list_from_file("Prob2-intcode-corrected.txt", sep=",")
prob2code = [int(x) for x in prob2text]

verbose_run(prob2code)

# print(len(prob2code))

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
