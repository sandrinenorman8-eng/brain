const App = () => {
    const [notes, setNotes] = React.useState([]);

    React.useEffect(() => {
        fetch('/api/knowledge-graph')
            .then(response => response.json())
            .then(data => {
                setNotes(data.data);
            });
    }, []);

    return <KnowledgeGraph notes={notes} />;
};

const domContainer = document.querySelector('#root');
ReactDOM.render(<App />, domContainer);
