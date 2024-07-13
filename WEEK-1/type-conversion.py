# Create a program that asks for user input and prints the type of input | For Int

value = input("Enter a value: ")

try:
    value = int(value)
except ValueError:
    try: 
        value = float(value)
    except ValueError:
        pass

print(f"You entered {value}, type is {type(value)}")
