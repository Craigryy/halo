import React, { useState, useEffect } from 'react';
import APIService from '../APIService';
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router-dom';

import '../CSS/Login.css'; // Import the external CSS file
import logp from '../images/logp.jpg'; // Import the background image

function Login() {
  // State variables
  const [username, setUserName] = useState('');
  const [password, setPassword] = useState('');
  const [isLogin, setLogin] = useState(true);
  const [token, setToken] = useCookies(['mytoken']);
  const [error, setError] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    /**
     * Checks if a valid token is present and navigates to the '/categories' page if available.
     *
     * @function
     * @returns {void}
     */
    const checkTokenAndNavigate = () => {
      if (token['mytoken']) {
        navigate('/categories');
      }
    };
  
    // Call the checkTokenAndNavigate function when the token or navigation function changes
    checkTokenAndNavigate();
  }, [token, navigate]);
  

/**
 * Handles login button click, validates input, sends login request, and sets token if successful.
 *
 * @async
 * @function
 * @returns {Promise<void>}
 */
const loginBtn = async () => {
  if (!username || !password) {
    setError('Please enter both username and password');
    return; // Exit early if fields are empty
  }

  const userData = { username, password };

  try {
    const token = await APIService.login(userData.username, userData.password);

    /**
     * Sets the authentication token in cookies and navigates to the '/categories' page on successful login.
     *
     * @function
     * @param {string} key - The key for the cookie.
     * @param {string} value - The value to set in the cookie.
     * @returns {void}
     */
    const setTokenAndNavigate = (key, value) => {
      setToken(key, value);
      navigate('/categories');
    };

    setTokenAndNavigate('mytoken', token);
  } catch (error) {
    if (error.response) {
      if (error.response.status === 401) {
        setError('Password is incorrect'); // Password is incorrect
      } else if (error.response.status === 404) {
        setError('Username is incorrect'); // Username is incorrect
      } else {
        setError('Either Username or Password is incorrect'); // Other errors
      }
    } else {
      setError('Login failed');
    }
    console.error('Login error:', error);
  }
};

/**
 * Handles register button click, validates input, sends user creation request, and navigates on success.
 *
 * @async
 * @function
 * @returns {Promise<void>}
 */
const registerBtn = async () => {
  let missingFields = [];

  if (!username) {
    missingFields.push('Username');
  }

  if (!password) {
    missingFields.push('Password');
  }

  if (missingFields.length > 0) {
    const errorMessage = `Please enter the following field(s): ${missingFields.join(', ')}`;
    setError(errorMessage);
    return; // Exit early if fields are missing
  }

  const userData = { username, password };

  try {
    await APIService.createUser(userData.username, userData.password);

    /**
     * Clears input fields and navigates to the '/categories' page on successful user creation.
     *
     * @function
     * @returns {void}
     */
    const clearFieldsAndNavigate = () => {
      setUserName('');
      setPassword('');
      setError('');
      navigate('/categories');
    };

    clearFieldsAndNavigate();

    console.log('User successfully created:', username);
  } catch (error) {
    setError('Error creating user');
    console.error('Error creating user:', error);
  }
};


  // JSX rendering
  return (
    <div className='login-page'>
      {/* Login Container */}
      <div className='login-container'>
        <img src={logp} alt='logp' className='login-image' />
        <h1 className='login-title'>{isLogin ? 'Login' : 'Register'}</h1>
        {error && <div className='login-error'>{error}</div>}
        <div className='mb-3'>
          <label htmlFor='username' className='login-label'>
            <i className='fas fa-user'></i> {/* Use Font Awesome icon for user */}
          </label>
          <input
            type='text'
            className='login-input'
            id='username'
            placeholder='Username'
            value={username}
            onChange={(e) => setUserName(e.target.value)}
          />
        </div>

        <div className='mb-3'>
          <label htmlFor='password' className='login-label'>
            <i className='fas fa-lock'></i> {/* Use Font Awesome icon for lock */}
          </label>
          <input
            type='password'
            className='login-input'
            id='password'
            placeholder='Password'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button
          href='#'
          onClick={isLogin ? loginBtn : registerBtn}
          className='login-button'
        >
          {isLogin ? 'Login' : 'Register'}
        </button>

        <div className='mb-3'>
          {isLogin ? (
            <h5>
              You don't have an account, please{' '}
              <a href='#' className='login-alt-button' onClick={() => setLogin(false)}>
                Sign up
              </a>{' '}
              here
            </h5>
          ) : (
            <h5>
              If you have an account,{' '}
              <a href='#' className='login-alt-button' onClick={() => setLogin(true)}>
                Login
              </a>{' '}
              here
            </h5>
          )}
        </div>
      </div>
    </div>
  );
}

export default Login;

 
