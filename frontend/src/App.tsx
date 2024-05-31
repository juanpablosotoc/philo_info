import React from 'react';
// import logo from './logo.svg';
import './App.css';
import ShortTextInput from './components/short_text_input/index';
import PasswordInput from './components/password_input/index';

function App() {
  return (
    <div className="App">
      <ShortTextInput />
      <PasswordInput />
    </div>
  );
}

export default App;
