import React, {useState, useEffect} from 'react';
import Button from './Components/Button';
import './App.css';

function App() {
  const [data, setData] = useState([{}]);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    fetch('/api')
      .then((response) => response.json())
      .then((info) => setData(info));
  }, []);

  const handleSubmit = () => {
    setVisible(true);
  };

  return (
    <div className='App'>
      <div className='header'>
        <h1>CSE 142 Code Quality Checker</h1>
      </div>

      <div className='parent'>
        <div className='codeBlock'>
          <Button onClick={handleSubmit} content='submit' />
        </div>
        <div
          className={
            visible ? 'resultsBlockVisible' : 'resultsBlockHidden'
          }></div>
      </div>

      <div className='footer fixed-bottom'>
        <h4>© cse142 2020</h4>
      </div>
    </div>
  );
}

export default App;
