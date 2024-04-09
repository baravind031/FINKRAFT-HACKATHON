document.addEventListener('DOMContentLoaded', function() {
    // Initialize ag-Grid
    var gridOptions = {
        columnDefs: [
            {
                headerName: "Transaction ID",
                field: "TransactionID",
                editable: false
            },
            {
                headerName: "Customer Name",
                field: "CustomerName",
                editable: true
            },
            {
                headerName: "Transaction Date",
                field: "TransactionDate",
                editable: true
            },
            {
                headerName: "Amount",
                field: "Amount",
                editable: true
            },
            {
                headerName: "Status",
                field: "Status",
                editable: true
            },
            {
                headerName: "Actions",
                cellRenderer: actionCellRenderer
            }
        ],
        defaultColDef: {
            flex: 1,
            minWidth: 100,
            resizable: true
        },
        rowSelection: 'single', // Allow only single row selection
        onCellValueChanged: onCellValueChanged // Callback function for cell value changes
    };

    // Get transactions data and populate ag-Grid
    fetch('/transactions')
        .then(response => response.json())
        .then(data => {
            var transactionsGrid = document.getElementById('transactionsGrid');
            new agGrid.Grid(transactionsGrid, gridOptions);
            gridOptions.api.setRowData(data);
        })
        .catch(error => console.error('Error:', error));

    // Define action cell renderer for edit and delete buttons
    function actionCellRenderer(params) {
        return `<button onclick="editTransaction(${params.data.id})">Edit</button>
                <button onclick="deleteTransaction(${params.data.id})">Delete</button>`;
    }

    // Function to handle cell value changes
    function onCellValueChanged(event) {
        var updatedData = event.data;
        fetch(`/transactions/${updatedData.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error updating transaction');
            }
            return response.json();
        })
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    }

    // Function to edit a transaction
    window.editTransaction = function(id) {
        var transaction = gridOptions.api.getRowNode(id).data;
        // You can implement your edit logic here
        console.log('Editing transaction:', transaction);
    };

    // Function to delete a transaction
    window.deleteTransaction = function(id) {
        if (confirm('Are you sure you want to delete this transaction?')) {
            fetch(`/transactions/${id}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error deleting transaction');
                }
                return response.json();
            })
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
        }
    };
});
