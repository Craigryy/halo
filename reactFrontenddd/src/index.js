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
import User from './components/User';

function Router() {
  const [users,setUsers]= useState([]);
  const [token, setToken, removeCookie] = useCookies(['mytoken']);

  const fetchUsers = () => {
    fetch('http://127.0.0.1:5000/users/', {
      method: 'GET',
      headers: {
        "Content-Type": 'application/json',
        "Authorization": `Bearer ${token['mytoken']}`
      }
    })
      .then(resp => resp.json())
      .then(resp => setUsers(resp))
      .catch(error => console.log(error));
  }
  
  

  const deleteBtnUser = (user)=>{
    const new_user = users.filter(myuser=>myuser.id !== user.id);
    setUsers(new_user);
    fetchUsers();
  }
  return (
    <CookiesProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          {/* Use the 'element' prop to render components */}
          <Route path="/categories" element={<App />} />
          <Route path='/user' element={<User/>} deleteBtnUser={deleteBtnUser}/>
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