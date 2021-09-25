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
import SubredditBody from './components/SubredditBody';
import CreatePostBody from './components/CreatePostBody';
import ErrorPage from './components/ErrorPage';

const App = () => {
  const [cookies, setCookie, removeCookie] = useCookies(["token", "loggedIn", "username"]);

  const handleLogin = (token, username) => {
    setCookie("token", token, { path: '/' });
    setCookie("loggedIn", true, { path: '/' });
    setCookie("username", username, {path: '/'});
  };

  const handleLogout = () => {
    removeCookie("token", { path: '/' });
    removeCookie("loggedIn", { path: '/' });
    removeCookie("username", { path: '/' });
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
        <Route path={"/r/"} component={() => <SubredditBody cookies={cookies}/>} />
        <Route exact path={"/404"} component={ErrorPage} />
          <Redirect to="/404" />
      </Switch>
    </Router>
  );
}

export default App;