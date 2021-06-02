import logo from './logo.svg';
import './App.css';
import Header from './components/Header';
import FrontpageBody from './components/FrontpageBody';




const App = () => {
  return (
    <div className="container">
      <Header />
      <FrontpageBody />
    </div>
  );
}

export default App;
