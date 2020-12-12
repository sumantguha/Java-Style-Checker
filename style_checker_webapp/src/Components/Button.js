import React from 'react';
import './Button.css';

function SubmitButton({content, onClick}) {
  return (
    <button onClick={onClick} className='button'>
      <h4 className='content-info'>{content}</h4>
    </button>
  );
}

export default SubmitButton;
