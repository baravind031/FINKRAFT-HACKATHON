# Transactions Management System
This is a Flask-based web application for managing transactions. Users can upload CSV files containing transaction data, view transactions in a table, edit transaction details, and delete transactions.

Features
Upload CSV files containing transaction data
View transactions in a table format
Edit transaction details
Delete transactions

Setup
Clone the Repository:
git clone <repository-url>

Database Configuration:

Make sure you have MySQL installed and running.

Create a MySQL database name.

## Update the database configuration in app.py if needed:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/database_name'

# Run the Application:
python app.py

# Usage
Upload CSV File:

Navigate to the home page and click on the "Upload CSV File" section.
Choose a CSV file containing transaction data and click the "Upload" button.
View Transactions:

Transactions will be displayed in a table format on the home page.
Each row will have edit and delete buttons.
Edit Transaction:

Click on the "Edit" button corresponding to the transaction you want to edit.
Update the transaction details in the modal or form that appears.
Delete Transaction:

Click on the "Delete" button corresponding to the transaction you want to delete.
Confirm the deletion when prompted
