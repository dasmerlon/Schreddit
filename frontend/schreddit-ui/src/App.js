import React from 'react';
import './App.css';
import Header from './components/Header';
import { useCookies } from 'react-cookie';
import FrontpageBody from './components/FrontpageBody';




const App = () => {
  const [cookies, setCookie, removeCookie] = useCookies(["token", "loggedIn"]);

  const handleLogin = token => {
    setCookie("token", token, { path: '/' });
    setCookie("loggedIn", true, { path: '/' });
  };

  return (
    <div className="container">
      <Header cookies={cookies} handleLogin={handleLogin} />
      <FrontpageBody />
    </div>
  );
}

export default App;
