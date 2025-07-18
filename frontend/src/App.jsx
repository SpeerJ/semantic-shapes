import './app.css'
import VectorArithmetic from "./VectorArithmetic.jsx";

function App() {
    return (
        <div>
            <header className="header">
                <h1>Semantic Shapes</h1>
            </header>
            <main style={{padding: '20px'}}>
                <div className="content-container">
                    <div>
                        This application demonstrates vector arithmetic on word embeddings.
                        Inspired by Word2Vec's ability to solve analogies like "king - man + woman = queen",
                        you can enter similar expressions below to find words closest to the resulting vector.
                    </div>
                    <VectorArithmetic/>
                    <div style={{textAlign: 'left', marginTop: '20px'}}>
                        Some interesting examples:
                        <ul>
                            <li>"animal + culpable ≈ human"</li>
                            <li>"tokyo - japan + france ≈ paris"</li>
                            <li>"walking - walk + swim ≈ swimming"</li>
                        </ul>
                    </div>
                </div>
            </main>
        </div>
    )
}

export default App;
