import './App.css';
import { BrowserRouter as Router, Route, Switch, Link, Redirect} from 'react-router-dom';
// We use this Router-Package: https://reactrouter.com/
import React from 'react';
import './App.css';
import logo from './images/schreddit.svg';
import Header from './components/header/Header';
import { useCookies } from 'react-cookie';



// Pages
import FrontpageBody from './components/FrontpageBody';
import Subredit from './components/Subredit';
import CreateSubreddit from './components/subreddit/CreateSubreddit'
import ErrorPage from './components/ErrorPage';

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
    <Router>
      <Header cookies={cookies} handleLogin={handleLogin} handleLogout={handleLogout} />
      <Switch>
        <Route exact path={"/"} component={FrontpageBody} />
        <Route path={"/r/"} component={Subredit} />
        <Route path={"/createSubreddit"} component={() => <CreateSubreddit cookies={cookies}/>}/>
        <Route exact path={"/404"} component={ErrorPage} />
          <Redirect to="/404" />
      </Switch>
    </Router>
  );
}

export default App;