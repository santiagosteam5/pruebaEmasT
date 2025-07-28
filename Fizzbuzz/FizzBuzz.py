def FizzBuzz(n):
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

def main():
    try:
        n = int(input("Ingrese un número entero positivo: "))
        FizzBuzz(n)
    except ValueError:
        print("Por favor, ingrese un número entero positivo.")

if __name__ == "__main__":
    main()