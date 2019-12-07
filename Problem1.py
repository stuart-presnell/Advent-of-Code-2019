from math import floor
def fuel(mass):
    return int(floor(mass/3)) - 2

# masses = [12, 14, 1969, 100756]
# fuels = [fuel(m) for m in masses]

# print(fuels)

f = open("Prob1-masses.txt")
massestext = f.read()
f.close()

masseslist = massestext.split('\n')
# print(type(masseslist[0]))
fuellist = [fuel(int(m))  for m in masseslist]

print(sum(fuellist))