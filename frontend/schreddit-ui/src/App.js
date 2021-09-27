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
  
  const [showLogin, setShowLogin] = React.useState(false);

  const handleLogin = (token, username) => {
    setCookie("token", token, { path: '/' });
    setCookie("username", username, {path: '/'});
    setCookie("loggedIn", true, { path: '/' });
  };

  const handleLogout = () => {
    removeCookie("token", { path: '/' });
    removeCookie("loggedIn", { path: '/' });
    removeCookie("username", { path: '/' });
    // window.location.reload();
  };

  return (
    <Router>
      <Header cookies={cookies} handleLogin={handleLogin} handleLogout={handleLogout} showLogin={showLogin} setShowLogin={setShowLogin}/>
      <Switch>
        <Route exact path={"/"} component={() => <FrontpageBody cookies={cookies} handleLogout={handleLogout} setShowLogin={setShowLogin} />} />
        <Route path={"/createSubreddit"} component={() => <CreateSubreddit cookies={cookies} handleLogout={handleLogout} setShowLogin={setShowLogin} />}/>
        <Route path={"/submit"} component={() => <CreatePostBody cookies={cookies} handleLogout={handleLogout} setShowLogin={setShowLogin}/>} />
        <Route path={"/settings/account"} component={() => <UserSettingsBody cookies={cookies} handleLogout={handleLogout} setShowLogin={setShowLogin}/>}/>
        <Route path={"/r/"} component={() => <SubredditBody cookies={cookies} handleLogout={handleLogout} setShowLogin={setShowLogin}/>} />
        <Route exact path={"/404"} component={ErrorPage} />
          <Redirect to="/404" />
      </Switch>
    </Router>
  );
}

export default App;