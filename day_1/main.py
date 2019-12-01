

def get_fuel_required(module_mass):
    return module_mass / 3 - 2

def fuel_counter_upper(path):
    total = 0
    f = open(path)
    for line in f:
        fuel_required = get_fuel_required(int(line))
        while(fuel_required > 0):
            total += fuel_required
            fuel_required = get_fuel_required(int(fuel_required))
    return total

path = "module_data.dat"
total = fuel_counter_upper(path)
print(total)