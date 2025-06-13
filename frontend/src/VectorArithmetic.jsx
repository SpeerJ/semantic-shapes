import React, {useState} from 'react';
import config from "./config.js";
import './vectorArithmetic.css';

function VectorArithmetic() {
    const [expression, setExpression] = useState('');
    const [results, setResults] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async () => {
        if (!expression.trim()) {
            setError('Please enter an expression');
            setResults([]);
            return;
        }
        setIsLoading(true);
        setError(null);
        setResults([]);

        try {
            const response = await fetch(`${config.apiBaseUrl}/api/arithmetic?expr=${encodeURIComponent(expression)}`);
            if (!response.ok) {
                let errorMsg = `HTTP error! status: ${response.status}`;
                try {
                    const errorData = await response.json();
                    if (errorData && errorData.detail && Array.isArray(errorData.detail) && errorData.detail.length > 0) {
                        errorMsg = errorData.detail.map(err => err.msg || 'Unknown error').join('; ');
                    } else if (errorData && errorData.detail && typeof errorData.detail === 'string') {
                        errorMsg = errorData.detail;
                    }
                } catch (jsonError) {
                    const textResponse = await response.text().catch(() => 'Could not read error body.');
                    errorMsg = `JSON error! status: ${response.status}, text: ${textResponse}`;
                }
                throw new Error(errorMsg);
            }
            const data = await response.json();
            const words = data.results;
            if (!Array.isArray(words) || (words.length > 0 && (!words[0].word || typeof words[0].similarity === 'undefined'))) {
                console.warn(`API response format might not contain expected word and similarity attributes: ${JSON.stringify(words)}`);
            }
            setResults(words);
        } catch (e) {
            setError(e.message || 'Failed to fetch results. Please check the console for more details.');
            setResults([]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            handleSubmit();
        }
    };

    return (
        <div style={{fontFamily: 'Arial, sans-serif', margin: '20px'}}>
            <div style={{
                display: 'flex',
                alignItems: 'center',
                width: '100%',
                marginBottom: '20px',
                borderLeft: '2px solid #377829',
                borderRadius: '4px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
                <input
                    type="text"
                    value={expression}
                    onChange={(e) => setExpression(e.target.value)}
                    onKeyDown={handleKeyPress}
                    placeholder="E.g., king - man + woman"
                    aria-label="Vector arithmetic expression"
                    style={{
                        flexGrow: 1,
                        padding: '10px',
                        border: '0px',
                        fontSize: '16px'
                    }}
                />
                <button
                    onClick={handleSubmit}
                    disabled={isLoading}
                    title="Run Expression"
                    style={{
                        padding: '10px 15px',
                        backgroundColor: isLoading ? '#ccc' : '#377829',
                        color: 'white',
                        marginRight: '1px',
                        cursor: isLoading ? 'default' : 'pointer',
                        fontSize: '18px',
                        lineHeight: '1',
                        transition: 'background-color 0.2s ease'
                    }}
                >
                    {isLoading ? '...' : '▶'}
                </button>
            </div>

            {error && <p style={{color: 'red', marginTop: '10px'}}>Error: {error}</p>}

            {results && results.length > 0 && (
                <div style={{marginTop: '20px'}}>
                    <h4>Results:</h4>
                    <table className="result-table">
                        <thead>
                        <tr>
                            <th className="table-header">Word</th>
                            <th className="table-header">similarity</th>
                        </tr>
                        </thead>
                        <tbody>
                        {results.map((result, i) => (
                            <tr key={i} className={i % 2 === 0 ? 'table-row-even' : 'table-row-odd'}>
                                <td className="table-cell">{result.word}</td>
                                <td className="table-cell">{typeof result.similarity === 'number' ? result.similarity.toFixed(5) : String(result.similarity)}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    )
}

export default VectorArithmetic;
