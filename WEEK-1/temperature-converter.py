# Temperature conversion functions (Celsius to Fahrenheit and vice versa).

#5 / 9 (F - 32)     |  F = 32 + 9 / 5 C

# Ask user which conversion is to be done?

operation = int(input("Which operation do your want to perform? \n 1. Cel to Far \n 2. Far to Cel\n "))


def celcius_fareheit(value):
    LH = 5 / 9
    RH = value - 32
    result = LH * RH
    print(f"{result} F")

def fareheit_celcius(value):
    LH = 32
    RH = 1.8 * value
    result = LH + RH
    print(f"{result} C")

if operation == 1:
    celcius_value = int(input("Enter Celsius Value: "))
    celcius_fareheit(celcius_value)
elif operation == 2:
    fareheit_value = int(input("Enter fareheit Value: "))
    fareheit_celcius(fareheit_value)
else:
    print("Kindly Select The Right Option.")