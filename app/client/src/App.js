// Styles
import './App.css';
import 'bulma/css/bulma.css'

// Components
import Banner from './components/Banner';
import Editor from './components/Editor';
import Result from './components/Result';
import Footer from './components/Footer';

function App() {
  return (
    <div className="App container">
      <Banner/>
      <div className="columns">
        <Editor/> 
        <Result/>
      </div>
      <Footer/>
    </div>
  );
}

export default App;
