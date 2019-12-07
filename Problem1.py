from math import floor

def list_from_file(filename, sep='\n'):
    """Return the content of the named file as a list of strings"""
    f = open("Prob1-masses.txt")
    file_content = f.read()
    f.close()
    return file_content.split(sep)

def fuel(mass):
    return int(floor(mass/3)) - 2

# Testing the function on the specified values:
# masses = [12, 14, 1969, 100756]
# fuels = [fuel(m) for m in masses]
# print(fuels)

masseslist = list_from_file("Prob1-masses.txt")
fuellist = [fuel(int(m))  for m in masseslist]

print(sum(fuellist))

def fuel_or_zero(mass):
    """Round up the fuel to zero if it's below zero"""
    return max(0,fuel(mass))

def iterated_fuel(mass):
    """Return a list of all the stages of fuel needed"""
    f = [fuel_or_zero(mass)]    # Start with the fuel for the initial mass
    while f[-1] > 0:            # Until the fuel to be added is zero ...
        f.append(fuel_or_zero(f[-1])) # add the fuel needed for the previous block of fuel
    return f

def total_fuel(mass):
    return sum(iterated_fuel(mass))

# Testing the function on the specified values:
# for x in [14, 1969, 100756]:
#     print(iterated_fuel(x), sum(iterated_fuel(x)))

total_fuel_list = [total_fuel(int(m))  for m in masseslist]

print(sum(total_fuel_list))
