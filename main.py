from lib import *

num_of_loads = int(input("Enter the number of loads:"))
init_input = [0.0] * num_of_loads
loads_ph_a = [0] * num_of_loads
loads_ph_b = [0] * num_of_loads
loads_ph_c = [0] * num_of_loads

for i in range(num_of_loads):
    init_input[i] = float(input(f"Input load {i}:"))

# Sorting Input Data by descending
sorted_input = sorted(init_input, reverse=True)

# Put Max value in minimum loaded phase
while sum(sorted_input):
    move_load_to_min_loaded_phase(loads_ph_a, loads_ph_b, loads_ph_c, sorted_input)
    move_load_to_min_loaded_phase(loads_ph_b, loads_ph_a, loads_ph_c, sorted_input)
    move_load_to_min_loaded_phase(loads_ph_c, loads_ph_a, loads_ph_b, sorted_input)

# Try achieve better results by flip near values
for i in range(3, num_of_loads - 1):
    sum_ph_a, sum_ph_b, sum_ph_c = get_sum_per_phase(loads_ph_a, loads_ph_b, loads_ph_c)
    max_in, min_in = get_max_and_min_per_phase(sum_ph_a, sum_ph_b, sum_ph_c)
    delta1 = max_in - min_in
    flip_near_phase(loads_ph_a, loads_ph_b, loads_ph_c, i)
    sum_ph_a, sum_ph_b, sum_ph_c = get_sum_per_phase(loads_ph_a, loads_ph_b, loads_ph_c)
    max_in, min_in = get_max_and_min_per_phase(sum_ph_a, sum_ph_b, sum_ph_c)
    delta2 = max_in - min_in
    if delta2 < delta1:
        continue
    else:
        flip_near_phase(loads_ph_a, loads_ph_b, loads_ph_c, i)

sum_ph_a, sum_ph_b, sum_ph_c = get_sum_per_phase(loads_ph_a, loads_ph_b, loads_ph_c)
max_in, min_in = get_max_and_min_per_phase(sum_ph_a, sum_ph_b, sum_ph_c)

# Restore original sequence of elements (not sorted)
restore(loads_ph_a, init_input, num_of_loads)
restore(loads_ph_b, init_input, num_of_loads)
restore(loads_ph_c, init_input, num_of_loads)

# Give phase names for sequence
phase = phase_name_maker(loads_ph_a, loads_ph_b, loads_ph_c, num_of_loads)

print(phase)
print("\nUneven of phases loading, [%] =", 100 * (max_in - min_in) / max_in)
