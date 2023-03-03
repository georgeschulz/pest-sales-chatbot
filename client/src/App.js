//boilerplate libraries
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
//pages imports
import Home from './pages/home';
import LoginPage from './pages/login';
import Dashboard from './pages/dashboard';
//route imports
import PrivateRoutes from './components/routeprotection/privateroutes';
import RestrictedRoutes from './components/routeprotection/restrictedroutes';

function App() {
  return (
    <div className="App">
     <Router>
        <Routes>
          <Route elements={<RestrictedRoutes />}>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<LoginPage />} />
          </Route>
          <Route element={<PrivateRoutes />}>
            <Route path="/dashboard" element={<Dashboard />} />
          </Route>
        </Routes>
     </Router>
    </div>
  );
}

export default App;
