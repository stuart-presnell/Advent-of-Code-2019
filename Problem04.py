# Provided range:
lower = 234208
upper = 765869

target_range = range(lower,upper+1)

def int_to_list_of_digits(n):
    return [int(x) for x in str(n)]

def meets_criteria(n):
    n = int_to_list_of_digits(n)
    return has_double(n) and non_decreasing(n)

def has_double(n):
    """Given a list of ints, return true if Two adjacent digits are the same"""
    for i in range(len(n)-1):
        if n[i] == n[i+1]:
            return True
    return False

def non_decreasing(n):
    """Given a list of ints, return true if Going from left to right the digits never decrease"""
    for i in range(len(n)-1):
        if n[i] > n[i+1]:
            return False
    return True

def chunk(L):
    """Given a list, break into chunks of identical runs"""
    chunks = []
    p=1
    for i in range(len(L)-1):
        if L[i] == L[i+1]:
            p+=1
        else:
            chunks.append(p)
            p=1
    chunks.append(p)
    return chunks


def has_exact_double(n):
    """Given a list of ints, return true if exactly two adjacent digits are the same"""
    return 2 in chunk(n)

def meets_criteria_b(n):
    n = int_to_list_of_digits(n)
    return has_exact_double(n) and non_decreasing(n)


# print(
#     has_exact_double([1,2,2,2,5,5,5,1])
# )


# print(len([x for x in target_range if meets_criteria(x)]))
# Answer: 1246

print(len([x for x in target_range if meets_criteria_b(x)]))
# Answer: 814