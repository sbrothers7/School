a = ["book 1", "book 2", "book 3"]
b = [[10, 5, 13], [5, 14, 11], [5, 7, 12]]

res = ["", 0]

for i in range(len(a)):
    if sum(b[i]) > res[1]:
        res[1] = sum(b[i])
        res[0] = a[i]

print(f"{res[0]}\n{res[1]}")