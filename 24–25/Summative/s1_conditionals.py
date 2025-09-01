# -----------------------------------------
# Solution (with annotations)
# -----------------------------------------
n = int(input("Welcome to the Voltage-Current-Resistance Calculator!\n\nWhat are you trying to solve for?\n1 - Voltage\n2 - Current\n3 - Resistance\n"))
print()
data = [0] * 3 # we unfortunately have to declare these as the last array refers to some indexes
if n in (2, 3): data[0] = float(input("What is the voltage(volts)? "))
if n in (1, 3): data[1] = float(input("What is the current(amps)? "))
if n in (1, 2): data[2] = float(input("What is the resistance(ohms)? "))
# Instead of checking for each case of n, we check for two caes at once
ref = [
    ["voltage", round(data[1] * data[2], 2), "volts"], 
    ["current", round(data[0] / data[2], 2), "amps"], 
    ["resistance", round(data[0] / data[1], 2), "ohms"]
]
# for each possible case, the needed values for printing is stored in an array
print(f"\nThe {ref[n - 1][0]} is {ref[n - 1][1]} {ref[n - 1][2]}.")

# The "proper" way (using only concepts taught in class):
n = int(input("Welcome to the Voltage-Current-Resistance Calculator!\n\nWhat are you trying to solve for?\n1 - Voltage\n2 - Current\n3 - Resistance\n"))
if n == 1:
    i = float(input("What is the current(amps)? "))
    r = float(input("What is the resistance(ohms)? "))
    print(f"The voltage is {i * r} volts.")
elif n == 2:
    v = float(input("What is the voltage(volts)? "))
    r = float(input("What is the resistance(ohms)? "))
    print(f"The current is {v / r} amps.")
elif n == 3:
    v = float(input("What is the voltage(volts)? "))
    i = float(input("What is the current(amps)? "))
    print(f"The resistance is {v / i} ohms.")

