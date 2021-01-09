import React, {useState, useEffect, useRef} from 'react';
import SubmitButton from './Components/Button';
// import RadioButton from './Components/RadioButton';
import './App.css';
import AceEditor from 'react-ace';
import {Modal} from 'react-bootstrap';
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
import {Prism as SyntaxHighlighter} from 'react-syntax-highlighter';
import {nord} from 'react-syntax-highlighter/dist/esm/styles/prism';

import {
  ChakraProvider,
  Box,
  Heading,
  Text,
  Flex,
  Button,
  extendTheme,
  NumberInput,
  NumberInputField,
} from '@chakra-ui/react';

const config = {
  useSystemColorMode: false,
  initialColorMode: 'light',
};

const lightMode = extendTheme({config});

const App = () => {
  const [data, setData] = useState(null);
  const [didSubmit, setDidSubmit] = useState(false);
  const [theme, setTheme] = useState('solarized_dark');
  const [errors, setErrors] = useState(null);
  const [tabSize, setTabSize] = useState(4); // TODO: Send back tabSize
  // TODO: Weird errors with long lines and such

  const scrollToRef = useRef(null);

  const [modalShow, setModalShow] = useState(false);

  const {width, height} = useWindowDimensions();

  const _handleSubmit = async () => {
    console.log(data);
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
    setErrors(response);
  }, [didSubmit]);

  const getValue = (newValue) => {
    setData(newValue);
  };

  const ButtonGroup = (props) => {
    return (
      <Box>Hello</Box>
      // <Box {...props}>
      //   <RadioButton
      //     changed={(event) => {
      //       setTheme(event.target.value);
      //     }}
      //     id='1'
      //     isSelected={theme === 'monokai'}
      //     label='Monokai'
      //     value='monokai'
      //   />

      //   <RadioButton
      //     changed={(event) => {
      //       setTheme(event.target.value);
      //     }}
      //     id='2'
      //     isSelected={theme === 'github'}
      //     label='GitHub'
      //     value='github'
      //   />
      //   <RadioButton
      //     changed={(event) => {
      //       setTheme(event.target.value);
      //     }}
      //     id='3'
      //     isSelected={theme === 'tomorrow'}
      //     label='Tomorrow'
      //     value='tomorrow'
      //   />
      //   <RadioButton
      //     changed={(event) => {
      //       setTheme(event.target.value);
      //     }}
      //     id='4'
      //     isSelected={theme === 'kuroir'}
      //     label='Kuroir'
      //     value='kuroir'
      //   />
      //   <RadioButton
      //     changed={(event) => {
      //       setTheme(event.target.value);
      //     }}
      //     id='5'
      //     isSelected={theme === 'twilight'}
      //     label='Twilight'
      //     value='twilight'
      //   />
      //   <RadioButton
      //     changed={(event) => {
      //       setTheme(event.target.value);
      //     }}
      //     id='6'
      //     isSelected={theme === 'xcode'}
      //     label='Xcode'
      //     value='xcode'
      //   />
      //   <RadioButton
      //     changed={(event) => {
      //       setTheme(event.target.value);
      //     }}
      //     id='7'
      //     isSelected={theme === 'textmate'}
      //     label='Textmate'
      //     value='textmate'
      //   />
      //   <RadioButton
      //     changed={(event) => {
      //       setTheme(event.target.value);
      //     }}
      //     id='8'
      //     isSelected={theme === 'solarized_dark'}
      //     label='Solarized Dark'
      //     value='solarized_dark'
      //   />
      //   <RadioButton
      //     changed={(event) => {
      //       setTheme(event.target.value);
      //     }}
      //     id='9'
      //     isSelected={theme === 'solarized_light'}
      //     label='Solarized Light'
      //     value='solarized_light'
      //   />
      //   <RadioButton
      //     changed={(event) => {
      //       setTheme(event.target.value);
      //     }}
      //     id='10'
      //     isSelected={theme === 'terminal'}
      //     label='Terminal'
      //     value='terminal'
      //   />
      // </Box>
    );
  };

  return (
    <ChakraProvider theme={lightMode}>
      <Box
        w='100%'
        bg='white'
        color='gray.900'
        display='flex'
        pb={10}
        flexDirection='column'>
        <Flex
          maxH='5vh'
          ml={20}
          mr={20}
          mt={10}
          justifyContent='space-between'
          alignItems='center'>
          <Heading fontWeight='700' fontSize='2xl'>
            CSE 14x Code Quality Checker
          </Heading>
          <Button
            variant='solid'
            colorScheme='blue'
            onClick={() => setModalShow(true)}>
            Help
          </Button>
        </Flex>
        <ButtonGroup
          marginTop={5}
          display='flex'
          flexDirection='row'
          justifyContent='space-around'
          mx='auto'
        />
        <Box mt={5} ml={20} maxH='70vh'>
          <AceEditor
            mode='java'
            theme={theme}
            setOptions={{
              enableBasicAutocompletion: true,
              enableLiveAutocompletion: true,
              enableSnippets: true,
              showPrintMargin: false,
            }}
            fontSize={16}
            // defaultValue=''
            height='70vh'
            width={width - 200}
            onChange={getValue}
            placeholder="Paste your program's source code here..."
          />
        </Box>
        <Flex ml={20} mt={5} maxW={width - 220}>
          <SubmitButton
            content='Check'
            onClick={() => {
              setDidSubmit(true);
              if (scrollToRef && scrollToRef.current) {
                scrollToRef.current.scrollIntoView({
                  behavior: 'smooth',
                });
              }
            }}
          />
          <Box>
            <NumberInput color='white'>
              <NumberInputField
                defaultValue={4}
                h='7vh'
                ml={5}
                bg='#f76c6c'
                textAlign='center'
                color='white'
                placeholder='Tab Size'
                borderRadius={10}
                id='tabsize'
                onChange={(e) => setTabSize(+e.target.value)}
              />
            </NumberInput>
          </Box>
        </Flex>
      </Box>
      {/*

        <div className='main'>
          
          <div className='bottom'>
            <SubmitButton
              content='Check'
              onClick={() => {
                setDidSubmit(true);
                if (scrollToRef && scrollToRef.current) {
                  scrollToRef.current.scrollIntoView({
                    behavior: 'smooth',
                  });
                }
              }}
            />
            <input
              type='text'
              placeholder='Tab Size'
              id='tabsize'
              onChange={(e) => setTabSize(+e.target.value)}
            />
          </div>
        </div>

        {errors && <Result errors={errors} scrollToRef={scrollToRef}></Result>}

        <div className='footer'>
          <h4>© cse142 2020</h4>
        </div>

        <HelpModal show={modalShow} onHide={() => setModalShow(false)} />
      </Box> */}
    </ChakraProvider>
  );
};

const HelpModal = (props) => {
  return (
    <Modal
      {...props}
      size='lg'
      aria-labelledby='contained-modal-title-vcenter'
      centered>
      <Modal.Header closeButton>
        <Modal.Title id='contained-modal-title-vcenter'>
          Instructions and Disclaimer
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <p>
          <b>
            <i>NOTE: Use this tool at your own risk.</i>
          </b>
          We do not guarantee that using this tool will cause you to avoid
          errors on an assignment. We makes no guarantees that what is found by
          this tool will encompass all possible style issues in the input code,
          so make sure to give your code a second look yourself
        </p>
      </Modal.Body>
      <Modal.Footer>
        <Button variant='info' onClick={props.onHide}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

const Result = ({errors, scrollToRef}) => {
  if (errors.length > 0) {
    return (
      <div>
        <h4 ref={scrollToRef} className='errorSummary'>
          Error Summary:{' '}
        </h4>
        {errors.map((error) => {
          return (
            <Card
              category={error[0]}
              line_num={error[1]}
              times={error[2]}
              message={error[3]}
              line={error[4]}
            />
          );
        })}
      </div>
    );
  } else {
    return (
      <div className='errors' ref={scrollToRef}>
        <h3>Error Summary: </h3>
        <h4>Looks good :)</h4>
      </div>
    );
  }
};

const Card = ({category, line_num, times, message, line}) => {
  line = line.trim();
  let forbidden = false;
  if (category.startsWith('[FORBIDDEN]')) {
    forbidden = true;
    category = category.substring(category.indexOf(' '));
  }
  return (
    <div className='align-left'>
      <div className='card'>
        <h5 className='card-header'>
          <b className={forbidden ? 'forbidden' : 'none'}>{category}</b> (line{' '}
          {line_num})
        </h5>
        <div className='card-body'>
          <SyntaxHighlighter style={nord} language='java'>
            {line}
          </SyntaxHighlighter>
          <p className='card-text'>{message}</p>
        </div>
      </div>
    </div>
  );
};

const getWindowDimensions = () => {
  const {innerWidth: width, innerHeight: height} = window;
  return {
    width,
    height,
  };
};

const useWindowDimensions = () => {
  const [windowDimensions, setWindowDimensions] = useState(
    getWindowDimensions()
  );

  useEffect(() => {
    function handleResize() {
      setWindowDimensions(getWindowDimensions());
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowDimensions;
};

export default App;
