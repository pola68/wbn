def calculator(num1, operator, num2):
	if operator == "+":
		return num1 + num2
	elif operator == "-":
		return num1 - num2
	elif operator == "*":
		return num1 * num2
	elif operator == "/":
		return num1 / num2
	else:
		return False


num1 = float(input("First number: "))
operator = input("What operation: ")
num2 = float(input("Second number: "))

print(calculator(num1, operator, num2))


