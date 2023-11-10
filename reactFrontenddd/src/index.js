import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { CookiesProvider } from 'react-cookie'; 
import { useCookies } from 'react-cookie';




import Login from './components/login';

function Router() {
  const [users,setUsers]= useState([]);
  const [token, setToken, removeCookie] = useCookies(['mytoken']);


  return (
    <CookiesProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          {/* Use the 'element' prop to render components */}
          <Route path="/categories" element={<App />} />
        </Routes>
      </BrowserRouter>
    </CookiesProvider>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router />
  </React.StrictMode>
);

reportWebVitals();