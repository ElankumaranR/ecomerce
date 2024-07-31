# E-commerce Platform

Welcome to the E-commerce Platform project! This project is designed to provide a full-featured e-commerce website using Python and MySQL.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Introduction

This E-commerce Platform is designed to facilitate online shopping. It allows users to browse products, add items to their cart, and make purchases. Administrators can manage products, categories, and orders.

## Features

- **User Authentication**: Secure sign-up and login for customers and administrators.
- **Product Management**: Add, edit, view, and delete products.
- **Category Management**: Organize products by categories.
- **Shopping Cart**: Add items to the cart and proceed to checkout.
- **Order Management**: View and manage orders.
- **Responsive Design**: Optimized for all devices, from desktops to mobile phones.

## Technologies Used

- **Python**: Programming language for backend development.
- **Flask**: Micro web framework for building the server and API.
- **MySQL**: Relational database for storing product and user data.
- **HTML5**: Markup language for creating the structure of the website.
- **CSS3**: Styling language for designing the layout and appearance.
- **JavaScript**: Programming language for interactive elements and functionality.
- **Bootstrap**: CSS framework for responsive design and pre-built components.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ElankumaranR/ecomerce.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd ecomerce
    ```

3. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Configure the database**:
    - Create a MySQL database named `ecommerce`.
    - Update the database connection settings in `config.py`:
    ```python
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/ecommerce'
    ```

6. **Initialize the database**:
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

7. **Run the application**:
    ```bash
    flask run
    ```

8. **Open your browser and visit** `http://localhost:5000` to see the application.

## Usage

- **Customers**: Sign up or log in to browse products, add items to the cart, and make purchases.
- **Administrators**: Sign up or log in to manage products, categories, and orders.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. **Fork the repository**.
2. **Create a new branch**:
    ```bash
    git checkout -b feature/your-feature
    ```
3. **Make your changes and commit them**:
    ```bash
    git commit -m "Add your feature"
    ```
4. **Push to the branch**:
    ```bash
    git push origin feature/your-feature
    ```
5. **Create a pull request**.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



Thank you for using the E-commerce Platform!
