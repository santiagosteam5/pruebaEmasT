def palindromo(s):
    s = s.lower().replace(" ", "").replace(",", "").replace(".", "").replace("!", "").replace("?", "").replace("¿", "").replace("¡", "")
    return s == s[::-1]

def main():
    try:
        s = input("Ingrese una palabra o frase: ")
        if palindromo(s):
            print(f"'{s}' es un palíndromo.")
        else:
            print(f"'{s}' no es un palíndromo.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()