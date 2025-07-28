def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
def main():
    try:
        n = int(input("Ingrese un numero entero positivo: "))
        print(f"La secuencia de Fibonacci hasta el {n} es:")
        for i in range(n + 1):
            print(fibonacci(i), end=' ')
    except ValueError:
        print("Por favor, ingrese un numero entero positivo.")

if __name__ == "__main__":
    main()