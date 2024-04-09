// frontend/src/components/FileUploadComponent.js

import React from 'react';
import axios from 'axios';

const FileUploadComponent = () => {
    const handleFileUpload = (e) => {
        const file = e.target.files[0];
        const formData = new FormData();
        formData.append('file', file);
        
        axios.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(response => {
            console.log(response.data.message);
        })
        .catch(error => {
            console.error('Error uploading file:', error);
        });
    };

    return (
        <div>
            <h2>Upload File</h2>
            <input type="file" onChange={handleFileUpload} />
        </div>
    );
};

export default FileUploadComponent;
