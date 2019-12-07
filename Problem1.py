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