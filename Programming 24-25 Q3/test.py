import random

r = random.randint(1, 100)
count = 0
while True:
    count += 1
    try:
        n = int(input("Enter guess: "))
    except:
        print("Incorrect format")
    if n == r:
        print(f"Correct.\n{count} tries taken.")
        break
    elif n > r:
        print("Number is smaller")
    else:
        print("Number is bigger")
