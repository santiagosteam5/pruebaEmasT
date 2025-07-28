def anagrama(w1, w2):
    return sorted(w1) == sorted(w2)

def main():
    try:
        w1 = input("Ingrese la primera palabra: ")
        w2 = input("Ingrese la segunda palabra: ")
        if anagrama(w1, w2):
            print(f"'{w1}' y '{w2}' son anagramas.")
        else:
            print(f"'{w1}' y '{w2}' no son anagramas.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()