# -----------------------
# Solution
# -----------------------
print("running solution (unpacked version)...")

n = int(input())
for i in range(n - 1): print("* " * (i + 1) + ". " * ((n - i - 2) * 2 + 1) + "* " * (i + 1))
print("* " * (n * 2 - 1))
for i in range(n - 2, -1 , -1): print("* " * (i + 1) + ". " * ((n - i - 2) * 2 + 1) + "* " * (i + 1))

# ------------------------------------------------
# More Straightforward Solution (with annotations)
# ------------------------------------------------
# print("running solution (extended version)...")

n = int(input())
for i in range(n - 1): 
    # repeat n - 1 times, since we want to print the middle row as just a row of stars
    # this is because the loop will print one extra star if we keep it as n
    print("* " * (i + 1), end="") 
    # the number of stars form a simple pattern of just {x ∈ ℕ: 0 < x <= n}
    print(". " * ((n - i - 1) * 2 - 1), end="") 
    # the number of dots form a pattern from the middle row to the top: 1, 3, 5, 7 ... (n - 1) * 2 - 1
    # to make this, we can simply subtract i from (n - 1) then multiply it by 2 and subtract 1 from the result
    print("* " * (i + 1))
    # lastly, the same star pattern occurs

    # in the original, these three print statements are merged into one
print("* " * (n * 2 - 1)) # print a row of stars
for i in range(n - 2, -1 , -1): 
    # for the inverse, we can just go through i in inverse
    print("* " * (i + 1), end="") 
    print(". " * ((n - i - 1) * 2 - 1), end="") 
    print("* " * (i + 1))

''' 
this solution uses two loops intentionally, 
as using the modulus operator to distinguish between 
the inverse and normal cases is actually slower.
instead of using loops to print the same characters, 
it uses string multiplication.
'''

