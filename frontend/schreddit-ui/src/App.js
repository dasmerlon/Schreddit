import './App.css';
import { BrowserRouter as Router, Route, Switch, Redirect} from 'react-router-dom';
// We use this Router-Package: https://reactrouter.com/
import React from 'react';
import './App.css';
import Header from './components/header/Header';
import UserSettingsBody from './components/user_settings/UserSettingsBody';
import { useCookies } from 'react-cookie';



// Pages
import FrontpageBody from './components/FrontpageBody';
import CreateSubreddit from './components/subreddit/CreateSubreddit'
import SubreditBody from './components/SubreditBody';
import CreatePostBody from './components/CreatePostBody';
import ErrorPage from './components/ErrorPage';

const App = () => {
  const [cookies, setCookie, removeCookie] = useCookies(["token", "loggedIn", "username", "email"]);

  const handleLogin = (token, type, data) => {
    setCookie("token", token, { path: '/' });
    setCookie("loggedIn", true, { path: '/' });
    setCookie(type, data, {path: '/'}); // saves username on login, but for email it saves "null"
  };

  const handleLogout = () => {
    removeCookie("token");
    removeCookie("loggedIn");
    removeCookie("username");
    removeCookie("email"); // That is why we need to remove email.
    window.location.reload();
  };

  return (
    <Router>
      <Header cookies={cookies} handleLogin={handleLogin} handleLogout={handleLogout} />
      <Switch>
        <Route exact path={"/"} component={() => <FrontpageBody cookies={cookies}/>} />
        <Route path={"/createSubreddit"} component={() => <CreateSubreddit cookies={cookies}/>}/>
        <Route path={"/submit"} component={() => <CreatePostBody cookies={cookies}/>} />
        <Route path={"/settings/account"} component={() => <UserSettingsBody cookies={cookies}/>}/>
        <Route path={"/r/"} component={() => <SubreditBody cookies={cookies}/>} />
        <Route exact path={"/404"} component={ErrorPage} />
          <Redirect to="/404" />
      </Switch>
    </Router>
  );
}

export default App;