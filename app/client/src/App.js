// Styles
import './App.css';
import 'bulma/css/bulma.css'

// Components
import Banner from './components/Banner';
import Editor from './components/Editor';
import Result from './components/Result';

function App() {
  return (
    <div className="App container">
      <Banner/>
      <div className="columns">
        <Editor/> 
        <Result/>
      </div>
    </div>
  );
}

export default App;
