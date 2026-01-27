from operations import add, substract, multiply, divide


# main loop
running = True

while running:
    cmd = input(
        "input two numbers and an operation (+,-,/,*) separated by a space or q to quit:"
    )
    if len(cmd) < 2:
        running = False
        break
    osat = cmd.split()
    num1 = osat[0]
    num2 = osat[1]
    operator = osat[-1]
    if operator == "+":
        print(add(num1, num2))
    if operator == "-":
        print(substract(num1, num2))
    if operator == "/":
        print(divide(num1, num2))
    if operator == "*":
        print(multiply(num1, num2))
