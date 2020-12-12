import React from 'react';
import './Button.css';

function Button({content, onClick}) {
  return (
    <button onClick={onClick} className='button'>
      <h4 className='content'>{content}</h4>
    </button>
  );
}

export default Button;
