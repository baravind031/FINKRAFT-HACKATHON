// frontend/src/App.js

import React from 'react';
import FileUploadComponent from './components/FileUploadComponent';
import TransactionsTableComponent from './components/TransactionsTableComponent';

const App = () => {
    return (
        <div>
            <h1>File Upload</h1>
            <FileUploadComponent />
            <h1>Transactions Table</h1>
            <TransactionsTableComponent />
        </div>
    );
};

export default App;
