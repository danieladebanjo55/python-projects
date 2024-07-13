# Simple calculator program

print("Hippie's Basic Calculator Program!")

a = int(input("Enter integer value for a: ")) 
b = int(input("Enter integer value for b: "))
operator = input("Enter an operator: e.g *, +, -, /: ")

if operator == '-':
    result = a - b
elif operator == '+':
    result = a + b
elif operator == '*':
    result = a * b
elif operator == '/':
    result = a / b
else:
    print("Please Enter a Valid OPerator!")

print(f"{a} {operator} {b} = {result}")
# print(result)