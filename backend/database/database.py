

create databse databse_name;
use database_name;

CREATE TABLE Transaction (
    TransactionID VARCHAR(255),
    CustomerName VARCHAR(255),
    TransactionDate DATE,
    Amount FLOAT,
    Status VARCHAR(50),
    InvoiceURL VARCHAR(255)
);

INSERT INTO `Transaction` VALUES ('TX10001','John Doe',	'2023-01-05',150,'Completed',	
'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf');
 