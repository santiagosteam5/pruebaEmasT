import sqlite3

class Item:
    def __init__(self, id, name, price):
        self.__id = id  # Private attribute
        self.__name = name  # Private attribute
        self.__price = price  # Private attribute
        self.__available = True  # Private attribute

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def is_available(self):
        return self.__available

    def set_name(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        self.__name = name.strip()

    def set_price(self, price):
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number")
        self.__price = price

    def set_availability(self, available):
        self.__available = bool(available)

    def mostrarInformacion(self):
        status = "Available" if self.__available else "Not Available"
        return f"ID: {self.__id}, Name: {self.__name}, Price: {self.__price}, Status: {status}"

    def to_dict(self):
        return {
            'id': self.__id,
            'name': self.__name,
            'price': self.__price,
            'type': self.__class__.__name__,
            'available': self.__available
        }

class Libro(Item):
    def __init__(self, id, name, price, author):
        super().__init__(id, name, price)
        self.__author = author  # Private attribute

    def get_author(self):
        return self.__author

    def set_author(self, author):
        if not isinstance(author, str) or not author.strip():
            raise ValueError("Author must be a non-empty string")
        self.__author = author.strip()

    def mostrarInformacion(self):
        return f"{super().mostrarInformacion()}, Author: {self.__author}"

    def to_dict(self):
        data = super().to_dict()
        data['author'] = self.__author
        return data

class Revista(Item):
    def __init__(self, id, name, price, issue):
        super().__init__(id, name, price)
        self.__issue = issue  # Private attribute

    def get_issue(self):
        return self.__issue

    def set_issue(self, issue):
        if not isinstance(issue, str) or not issue.strip():
            raise ValueError("Issue must be a non-empty string")
        self.__issue = issue.strip()

    def mostrarInformacion(self):
        return f"{super().mostrarInformacion()}, Issue: {self.__issue}"

    def to_dict(self):
        data = super().to_dict()
        data['issue'] = self.__issue
        return data

class BibliotecaDB:
    def __init__(self, db_name="biblioteca.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                type TEXT NOT NULL,
                available INTEGER NOT NULL DEFAULT 1,
                borrow_count INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                author TEXT NOT NULL,
                FOREIGN KEY (id) REFERENCES items (id) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY,
                issue TEXT NOT NULL,
                FOREIGN KEY (id) REFERENCES items (id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        conn.close()
        print(f"Database '{self.db_name}' initialized successfully!")

    def add_item(self, item):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO items (id, name, price, type, available, borrow_count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (item.get_id(), item.get_name(), item.get_price(), item.__class__.__name__, int(item.is_available()), 0))

            if isinstance(item, Libro):
                cursor.execute('''
                    INSERT INTO books (id, author)
                    VALUES (?, ?)
                ''', (item.get_id(), item.get_author()))

            elif isinstance(item, Revista):
                cursor.execute('''
                    INSERT INTO magazines (id, issue)
                    VALUES (?, ?)
                ''', (item.get_id(), item.get_issue()))

            conn.commit()
            print(f"{item.__class__.__name__} '{item.get_name()}' added to database!")

        except sqlite3.IntegrityError:
            print(f"Error: Item with ID {item.get_id()} already exists!")
        except Exception as e:
            print(f"Error adding item: {e}")
        finally:
            conn.close()

    def get_item_by_id(self, item_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        item_data = cursor.fetchone()

        if not item_data:
            conn.close()
            return None

        id, name, price, item_type, available, created_at, borrow_count = item_data

        if item_type == 'Libro':
            cursor.execute('SELECT author FROM books WHERE id = ?', (item_id,))
            author_data = cursor.fetchone()
            conn.close()
            if author_data:
                libro = Libro(id, name, price, author_data[0])
                libro.set_availability(bool(available))
                return libro

        elif item_type == 'Revista':
            cursor.execute('SELECT issue FROM magazines WHERE id = ?', (item_id,))
            issue_data = cursor.fetchone()
            conn.close()
            if issue_data:
                revista = Revista(id, name, price, issue_data[0])
                revista.set_availability(bool(available))
                return revista

        conn.close()
        item = Item(id, name, price)
        item.set_availability(bool(available))
        return item
    
    def get_all_items(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM items ORDER BY id')
        item_ids = cursor.fetchall()
        conn.close()
        
        items = []
        for (item_id,) in item_ids:
            item = self.get_item_by_id(item_id)
            if item:
                items.append(item)
        
        return items
    
    def delete_item(self, item_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
        
        if cursor.rowcount > 0:
            print(f"Item with ID {item_id} deleted successfully!")
        else:
            print(f"Item with ID {item_id} not found!")
        
        conn.commit()
        conn.close()
    
    def search_by_name(self, name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM items WHERE name LIKE ?', (f'%{name}%',))
        item_ids = cursor.fetchall()
        conn.close()
        
        items = []
        for (item_id,) in item_ids:
            item = self.get_item_by_id(item_id)
            if item:
                items.append(item)
        
        return items
    
    def show_database_stats(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM items')
        total_items = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM books')
        total_books = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM magazines')
        total_magazines = cursor.fetchone()[0]
        
        conn.close()
        
        print("\n" + "="*40)
        print("DATABASE STATISTICS")
        print("="*40)
        print(f"Total Items: {total_items}")
        print(f"Books: {total_books}")
        print(f"Magazines: {total_magazines}")
        print("="*40)
    
    def update_item_availability(self, item_id, available):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE items
                SET available = ?
                WHERE id = ?
            ''', (int(available), item_id))

            if cursor.rowcount > 0:
                print(f"Item with ID {item_id} availability updated to {'Available' if available else 'Not Available'}.")
            else:
                print(f"Item with ID {item_id} not found in the database.")

            conn.commit()
        except Exception as e:
            print(f"Error updating item availability: {e}")
        finally:
            conn.close()

    def update_borrow_count(self, item_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE items
                SET borrow_count = borrow_count + 1
                WHERE id = ?
            ''', (item_id,))

            if cursor.rowcount > 0:
                print(f"Borrow count updated for item with ID {item_id}.")
            else:
                print(f"Item with ID {item_id} not found in the database.")

            conn.commit()
        except Exception as e:
            print(f"Error updating borrow count: {e}")
        finally:
            conn.close()

class LibraryManager:
    def __init__(self):
        self.db = BibliotecaDB()

    def add_item(self, item):
        self.db.add_item(item)

    def borrow_item(self, item_id):
        item = self.db.get_item_by_id(item_id)
        if item:
            if item.is_available():
                item.set_availability(False)
                self.db.update_item_availability(item_id, False)
                self.db.update_borrow_count(item_id)
                print(f"Item '{item.get_name()}' has been borrowed.")
            else:
                print(f"Item '{item.get_name()}' is already borrowed.")
        else:
            print(f"Item with ID {item_id} not found.")

    def return_item(self, item_id):
        item = self.db.get_item_by_id(item_id)
        if item:
            if not item.is_available():
                item.set_availability(True)
                self.db.update_item_availability(item_id, True)
                print(f"Item '{item.get_name()}' has been returned.")
            else:
                print(f"Item '{item.get_name()}' was not borrowed.")
        else:
            print(f"Item with ID {item_id} not found.")

    def view_items(self):
        items = self.db.get_all_items()
        if items:
            print("\nLibrary Items:")
            for item in items:
                print(item.mostrarInformacion())
        else:
            print("No items in the library.")

    def list_available_items(self):
        items = self.db.get_all_items()
        available_items = [item for item in items if item.is_available()]
        if available_items:
            print("\nAvailable Items:")
            for item in available_items:
                print(item.mostrarInformacion())
        else:
            print("No items are currently available.")

    def find_borrowed_items(self):
        items = self.db.get_all_items()
        borrowed_items = [item for item in items if not item.is_available()]
        if borrowed_items:
            print("\nBorrowed Items:")
            for item in borrowed_items:
                print(item.mostrarInformacion())
        else:
            print("No items are currently borrowed.")

    def calculate_most_borrowed_item(self):
        conn = sqlite3.connect(self.db.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, name, MAX(borrow_count) AS max_borrowed
            FROM items
            WHERE borrow_count IS NOT NULL
        ''')
        result = cursor.fetchone()
        conn.close()

        if result and result[2] is not None:
            print(f"\nMost Borrowed Item: {result[1]} (ID: {result[0]}) with {result[2]} borrows.")
        else:
            print("No borrowing data available.")
