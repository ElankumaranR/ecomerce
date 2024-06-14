**E-Commerce Website using Flask and MySQL**
This project is an e-commerce website developed using Flask, Python, MySQL, HTML, and CSS.

**Introduction**
This repository contains the source code for an e-commerce website built with Flask and MySQL. The website allows users to browse products, add them to their cart, and checkout securely.

**Features**
User authentication (register, login, logout)
Product browsing by category
Product search functionality
Shopping cart management
Secure checkout process
Admin panel for product and user management
Responsive UI using HTML and CSS

**Requirements**
Python 3.x
Flask
Flask-MySQLdb
MySQL
HTML, CSS (Bootstrap is optional for UI enhancements)



Installation
Clone the repository:
git clone <repository-url>

Navigate into the project directory:
cd <project-directory>

Install dependencies using pip:
pip install -r requirements.txt

Set up MySQL database:
Make sure you have MySQL installed and running on your system.
Create a new database for the project.

Initialize the database schema:
Open a terminal and navigate to the project directory.

Run the following command to initialize the database schema:
python initialize_database.py

Configuration
Before running the application, make sure to configure the database connection in config.py:
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'your_mysql_username',
    'password': 'your_mysql_password',
    'database': 'your_database_name',
    'port': 3306  # Change this if your MySQL server is running on a different port
}

Usage
Start the Flask application:
python app.py
The application will start running on http://localhost:5000.
