# app.py

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import csv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# MySQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/vote'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   
app.config['UPLOAD_FOLDER'] = 'uploads'

 
# ALLOWED_EXTENSIONS = {'csv'}

db = SQLAlchemy(app)

class Transaction(db.Model):
    __tablename__ = 'transaction'  

    TransactionID = db.Column(db.Integer, primary_key=True)
    CustomerName = db.Column(db.String(255))
    TransactionDate = db.Column(db.Date)
    Amount = db.Column(db.Float)
    Status = db.Column(db.String(50))
    InvoiceURL = db.Column(db.String(255))


@app.route('/')
def index():
    return render_template('upload.html')
# Check if the file extension is allowed

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'
  
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            with open(file_path, 'r') as csv_file:
                csv_data = csv.DictReader(csv_file)
                for row in csv_data:
                    try:
                        transaction = Transaction(
                            TransactionID=int(row['TransactionID']),
                            CustomerName=row['CustomerName'],
                            TransactionDate=row['TransactionDate'],
                            Amount=float(row['Amount']),
                            Status=row['Status'],
                            InvoiceURL=row['InvoiceURL']
                        )   
                        db.session.add(transaction)
                    except ValueError:
                        # Skip invalid rows
                        continue

                db.session.commit()
            return jsonify({'message': 'File uploaded successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400
@app.route('/manual_entry', methods=['POST'])
def manual_entry():
    # Get data from the form
    transactionID = request.form['transactionID']
    customerName = request.form['customerName']
    transactionDate = request.form['transactionDate']
    amount = request.form['amount']
    status = request.form['status']
    invoiceURL = request.form['invoiceURL']

    try:
        # Create a new Transaction object and add it to the database
        transaction = Transaction(
            TransactionID=int(transactionID),
            CustomerName=customerName,
            TransactionDate=transactionDate,
            Amount=float(amount),
            Status=status,
            InvoiceURL=invoiceURL
        )
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'message': 'Data submitted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    result = [{'TransactionID': transaction.TransactionID, 
               'CustomerName': transaction.CustomerName, 
               'Amount': transaction.Amount, 
               'TransactionDate': transaction.TransactionDate.strftime('%Y-%m-%d'), 
               'Status': transaction.Status} 
              for transaction in transactions]
    return jsonify(result), 200

@app.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    data = request.get_json()
    try:
        transaction = Transaction.query.get(transaction_id)
        if transaction:
            # Update the transaction attributes with data from request JSON
            transaction.CustomerName = data.get('CustomerName', transaction.CustomerName)
            transaction.Amount = data.get('Amount', transaction.Amount)
            transaction.Status = data.get('Status', transaction.Status)
            transaction.TransactionDate = data.get('TransactionDate', transaction.TransactionDate)
            transaction.InvoiceURL = data.get('InvoiceURL', transaction.InvoiceURL)
            db.session.commit()
            return jsonify({'message': 'Transaction updated successfully'}), 200
        else:
            return jsonify({'error': 'Transaction not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        transaction = Transaction.query.get(transaction_id)
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
            return jsonify({'message': 'Transaction deleted successfully'}), 200
        else:
            return jsonify({'error': 'Transaction not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    db.create_all()
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
