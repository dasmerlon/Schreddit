import './App.css';
import { BrowserRouter as Router, Route, Switch, Link, Redirect} from 'react-router-dom';
// We use this Router-Package: https://reactrouter.com/


// Pages
import FrontpageBody from './components/FrontpageBody';
import Subredit from './components/Subredit';
import ErrorPage from './components/ErrorPage';

const App = () => {
  return (
    <Router>
      <Switch>
        <Route exact path={"/"} component={FrontpageBody} />
        <Route path={"/r/"} component={Subredit} />
        <Route exact path={"/404"} component={ErrorPage} />
          <Redirect to="/404" />
      </Switch>
    </Router>
  );
}

export default App;