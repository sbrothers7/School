# Accepted solution
a = input()

for i in range(len(a)):
    for j in range(i + 1):
        print(a[i], end="")
    for j in range(len(a) - 1 - i):
        print("*", end="")
    print()

# My solution
for i in range(len(a := input())): print(a[i] * (i + 1) + "*" * (len(a) - 1 - i))
