a = "D 120 W 120 D 50 W 50 D 25"
res = 0

for i in range(len(a)):
    n = ""
    count = 0

    for x in a[i + 2:]:
        if x == ' ': break
        n += x
        count += 1

    i += count
    if a[i - count] == 'D': res += int(n)
    elif a[i - count] == 'W': res -= int(n)
print(res)