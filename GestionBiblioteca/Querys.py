from Biblioteca import LibraryManager as LibraryManager

def main():
    manager = LibraryManager()

    # libro1 = Libro(1, "Don Quijote", 25.99, "Miguel de Cervantes")
    # libro2 = Libro(2, "Cien años de soledad", 18.50, "Gabriel García Márquez")
    # revista1 = Revista(3, "National Geographic", 8.99, "March 2024")
    # revista2 = Revista(4, "Scientific American", 12.99, "Issue 156")

    # manager.add_item(libro1)
    # manager.add_item(libro2)
    # manager.add_item(revista1)
    # manager.add_item(revista2)

    # manager.view_items()

    # manager.borrow_item(1)

    manager.list_available_items()

    manager.find_borrowed_items()

    manager.calculate_most_borrowed_item()

if __name__ == "__main__":
    main()