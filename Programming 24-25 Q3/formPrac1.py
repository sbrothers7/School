# -----------------------------------------
# Solution (with annotations)
# -----------------------------------------
print("Welcome to the PaySlip Calculator\n")
rate = int(input("Enter your hourly rate: "))
hours = int(input("How many hours did you work this week: "))
tax = ord(input("Enter your tax category: ").upper()) - 65
'''
Here, the letter grade for the input is first turned into uppercase,
then converted into ASCII code by using the ord() function. 
Since 'A' is 65, 'B' is 66 and so on, we can subtract 65 from these values
to use them as indexes.
'''
deductions = [0, 0.06, 0.15, 0.24, 0.35]
# store the amount of deductions corresponding to the tax category
if hours > 40: 
    print("\nGross Pay: $" + str(grossPay := rate * 40 + (rate * 2 * (hours - 40))))
    '''
    Here, grossPay gets asigned a value AND printed in the same line. 
    This is done by using the walrus operator, and since it initializes 
    variables not in the inner scope of the if statement, this is what
    allows us to reference it at the end of the program.
    '''
else: print("\nGross Pay: $" + str(grossPay := rate * hours)) # same thing here
print("Tax Deduction: $" + str(deduction := int(grossPay * deductions[tax])) + "\nNet Pay: $" + str(grossPay - deduction))
'''
In the last line, deduction is initilized as the the calculated value of 
grossPay minus the deductions according to the tax category, then since 
deduction is now a valid variable, it is possible to print the final 
value in the same line in the print statement
'''

# One-liner:
exec("print(\"Welcome to the PaySlip Calculator\\n\"); rate = int(input(\"Enter your hourly rate: \")); hours = int(input(\"How many hours did you work this week: \")); tax = ord(input(\"Enter your tax category: \").upper()) - 65; deductions = [0, 0.06, 0.15, 0.24, 0.35]\nif hours > 40: print(\"\\nGross Pay: $\" + str(grossPay := rate * 40 + (rate * 2 * (hours - 40))))\nelse: print(\"\\nGross Pay: $\" + str(grossPay := rate * hours))\nprint(\"Tax Deduction: $\" + str(deduction := int(grossPay * deductions[tax])) + \"\\nNet Pay: $\" + str(grossPay - deduction))")
