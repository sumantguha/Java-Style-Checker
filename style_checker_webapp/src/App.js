import React, {useState, useEffect} from 'react';
import SubmitButton from './Components/Button';
import RadioButton from './Components/RadioButton';
import './App.css';
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-java';
import 'ace-builds/src-noconflict/theme-github';
import 'ace-builds/src-noconflict/theme-monokai';
import 'ace-builds/src-noconflict/theme-tomorrow';
import 'ace-builds/src-noconflict/theme-kuroir';
import 'ace-builds/src-noconflict/theme-twilight';
import 'ace-builds/src-noconflict/theme-xcode';
import 'ace-builds/src-noconflict/theme-textmate';
import 'ace-builds/src-noconflict/theme-solarized_dark';
import 'ace-builds/src-noconflict/theme-solarized_light';
import 'ace-builds/src-noconflict/theme-terminal';
import 'ace-builds/src-noconflict/ext-language_tools';

function App() {
  const [data, setData] = useState(null);
  const [didSubmit, setDidSubmit] = useState(false);
  const [theme, setTheme] = useState('solarized_dark');
  const [errors, setErrors] = useState(null);

  const Result = ({props}) => {
    if (props != '[]') {
      let contents = props.split(',');
      for (let i = 0; i < contents.length - 3; i += 4) {
        var category = contents[i].slice(3, -1);
        var line_num = +contents[i + 1].slice(2, -1);
        var times = +contents[i + 2].slice(2, -1);
        var message = contents[i + 3].slice(2, -2);
        if (message.endsWith('"')) {
          message = message.slice(0, -1);
        }
      }
      return (
        <div className='dynamic'>
          <h6>Checking...</h6>
          <p>{category}</p>
          <p>{line_num}</p>
          <p>{times}</p>
          <p>{message}</p>
        </div>
      );
    } else {
      return (
        <div className='good'>
          <h6>Checking...</h6>
          <h4>Looks good :)</h4>
        </div>
      );
    }
  };

  const _handleSubmit = async () => {
    const response = await fetch('http://localhost:5000/code', {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return response.json();
  };

  useEffect(async () => {
    setDidSubmit(false);
    const response = await _handleSubmit();
    const error = response.result;
    setErrors(error);
  }, [didSubmit]);

  const getValue = (newValue) => {
    setData(newValue);
  };

  return (
    <div className='App'>
      <div className='header'>
        <h1>CSE 142 Code Quality Checker</h1>
      </div>
      {/* <Result category='Hello' line_num='10' times='30' message='Println' /> */}
      <div className='parent'>
        <div className='buttons'>
          <RadioButton
            changed={(event) => {
              setTheme(event.target.value);
            }}
            id='1'
            isSelected={theme === 'monokai'}
            label='Monokai'
            value='monokai'
          />

          <RadioButton
            changed={(event) => {
              setTheme(event.target.value);
            }}
            id='2'
            isSelected={theme === 'github'}
            label='GitHub'
            value='github'
          />
          <RadioButton
            changed={(event) => {
              setTheme(event.target.value);
            }}
            id='3'
            isSelected={theme === 'tomorrow'}
            label='Tomorrow'
            value='tomorrow'
          />
          <RadioButton
            changed={(event) => {
              setTheme(event.target.value);
            }}
            id='4'
            isSelected={theme === 'kuroir'}
            label='Kuroir'
            value='kuroir'
          />
          <RadioButton
            changed={(event) => {
              setTheme(event.target.value);
            }}
            id='5'
            isSelected={theme === 'twilight'}
            label='Twilight'
            value='twilight'
          />
          <RadioButton
            changed={(event) => {
              setTheme(event.target.value);
            }}
            id='6'
            isSelected={theme === 'xcode'}
            label='Xcode'
            value='xcode'
          />
          <RadioButton
            changed={(event) => {
              setTheme(event.target.value);
            }}
            id='7'
            isSelected={theme === 'textmate'}
            label='Textmate'
            value='textmate'
          />
          <RadioButton
            changed={(event) => {
              setTheme(event.target.value);
            }}
            id='8'
            isSelected={theme === 'solarized_dark'}
            label='Solarized Dark'
            value='solarized_dark'
          />
          <RadioButton
            changed={(event) => {
              setTheme(event.target.value);
            }}
            id='9'
            isSelected={theme === 'solarized_light'}
            label='Solarized Light'
            value='solarized_light'
          />
          <RadioButton
            changed={(event) => {
              setTheme(event.target.value);
            }}
            id='10'
            isSelected={theme === 'terminal'}
            label='Terminal'
            value='terminal'
          />
        </div>
      </div>
      <div className='manager'>
        <div className='main'>
          <AceEditor
            className='codeBlock'
            mode='java'
            theme={theme}
            setOptions={{
              enableBasicAutocompletion: true,
              enableLiveAutocompletion: true,
              enableSnippets: true,
            }}
            fontSize={16}
            defaultValue=''
            height='500px'
            width='750px'
            onChange={getValue}
            placeholder="Paste your program's source code here..."
          />
          <SubmitButton content='Submit' onClick={() => setDidSubmit(true)} />
        </div>
        {errors && <Result props={errors}></Result>}
      </div>

      <div className='footer fixed-bottom'>
        <h4>© cse142 2020</h4>
      </div>
    </div>
  );
}

export default App;
