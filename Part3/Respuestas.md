Respuesta 2.

Para implementar la funcionalidad de agregar al carrito una vez que este implementada la base de datos (relacional) de manera correcta el usuario podra tener su propio carrito al cual podra agregar los productos con la cantidad deseada

Respuesta 3.

CREATE TABLE User (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  email VARCHAR(100) UNIQUE,
  phone VARCHAR(20)
);

CREATE TABLE Product (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  price DECIMAL(10,2),
  stock INT
);

CREATE TABLE Cart (
  id INT PRIMARY KEY AUTO_INCREMENT,
  userId INT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (userId) REFERENCES User(id)
);

CREATE TABLE CartItem (
  id INT PRIMARY KEY AUTO_INCREMENT,
  cartId INT,
  productId INT,
  amount INT CHECK (amount > 0),
  FOREIGN KEY (cartId) REFERENCES Cart(id) ON DELETE CASCADE,
  FOREIGN KEY (productId) REFERENCES Product(id)
);

CREATE TABLE `Order` (
  id INT PRIMARY KEY AUTO_INCREMENT,
  userId INT,
  cartId INT,
  date DATETIME DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(50),
  total DECIMAL(10,2),
  FOREIGN KEY (userId) REFERENCES User(id),
  FOREIGN KEY (cartId) REFERENCES Cart(id)
);

CREATE TABLE Payment (
  id INT PRIMARY KEY AUTO_INCREMENT,
  orderId INT,
  paymentMethod VARCHAR(50),
  total DECIMAL(10,2),
  status VARCHAR(50),
  paymentDate DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (orderId) REFERENCES `Order`(id)
);
