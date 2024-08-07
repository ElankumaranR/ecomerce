
CREATE TABLE customer (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(20),
    email VARCHAR(220) NOT NULL,
    password_hash VARCHAR(225),
    date_joined DATETIME,
    PRIMARY KEY (id),
    UNIQUE (email)
);



CREATE TABLE item (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    current_price INT NOT NULL,
    previous_price INT NOT NULL,
    remaining INT NOT NULL,
    date_added DATETIME,
    image_url VARCHAR(255), 
    PRIMARY KEY (id)
);



CREATE TABLE cart_item (
    id INT NOT NULL AUTO_INCREMENT,
    customer_link INT NOT NULL,
    item_name VARCHAR(200) NOT NULL,
    price INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (customer_link) REFERENCES customer (id)
);



