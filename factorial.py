import math

def calculate_factorial(number):
    if number < 0:
        return "Factorial is not defined for negative numbers."
    return math.factorial(number)

if __name__ == "__main__":
    print("Enter a number to calculate its factorial:")
    number = int(input())
    result = calculate_factorial(number)
    print(f"The factorial of {number} is {result}")
