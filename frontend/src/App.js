// src/App.js

import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [file, setFile] = useState(null);
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleQueryChange = (e) => {
        setQuery(e.target.value);
    };

    const handleFileUpload = async () => {
        const formData = new FormData();
        formData.append('file', file);
    
        try {
            // Send the file to the backend /upload/ endpoint with an increased timeout
            await axios.post('http://localhost:8000/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                timeout: 30000, // Increase timeout to 30 seconds
            });
    
            alert('File uploaded successfully.');
        } catch (error) {
            console.error('Error uploading file:', error);
            alert('Failed to upload the file.');
        }
    };
    
    const handleQuerySubmit = async () => {
        try {
            const response = await axios.post('http://localhost:8000/query/', { query }, {
                headers: {
                    'Content-Type': 'application/json',
                },
                timeout: 30000, // Increase timeout to 30 seconds
            });
    
            setResponse(response.data.response);  // Assuming response.data.response contains the desired output
        } catch (error) {
            console.error('Error submitting query:', error);
            alert('Failed to submit the query.');
        }
    };
       
    
    return (
        <div>
            <h1>Document Upload and Query</h1>

            <div>
                <input type="file" onChange={handleFileChange} />
                <button onClick={handleFileUpload}>Upload File</button>
            </div>

            <div>
                <input
                    type="text"
                    value={query}
                    onChange={handleQueryChange}
                    placeholder="Enter your query"
                />
                <button onClick={handleQuerySubmit}>Submit Query</button>
            </div>

            {response && (
                <div>
                    <h2>Response</h2>
                    <p>{response}</p>
                </div>
            )}
        </div>
    );
}

export default App;
