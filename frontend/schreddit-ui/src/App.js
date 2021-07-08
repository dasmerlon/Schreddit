import React from 'react';
import './App.css';
import logo from './images/schreddit.svg';
import Header from './components/header/Header';
import { useCookies } from 'react-cookie';
import FrontpageBody from './components/FrontpageBody';




const App = () => {
  const [cookies, setCookie, removeCookie] = useCookies(["token", "loggedIn"]);

  const handleLogin = token => {
    setCookie("token", token, { path: '/' });
    setCookie("loggedIn", true, { path: '/' });
  };

  const handleLogout = () => {
    removeCookie("token");
    removeCookie("loggedIn")
    window.location.reload();
  };

  return (
    <div className="container">
      <Header cookies={cookies} handleLogin={handleLogin} handleLogout={handleLogout} logo={logo} />
      <FrontpageBody />
    </div>
  );
}

export default App;
