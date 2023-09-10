// import React, { useState, useEffect } from 'react';
// import APIService from '../APIService';
// import { useCookies } from 'react-cookie';
// import { useNavigate } from 'react-router-dom';
// import '../App.css'; 

// function Login() {
//   // State variables
//   const [username, setUserName] = useState('');
//   const [password, setPassword] = useState('');
//   const [isLogin, setLogin] = useState(true);
//   const [token, setToken] = useCookies(['mytoken']);
//   const [error, setError] = useState('');
//   const navigate = useNavigate();

//   // Effect to check for token and redirect if present
//   useEffect(() => {
//     if (token['mytoken']) {
//       navigate('/categories');
//     }
//   }, [token, navigate]);

//   // Login button click handler
//   const loginBtn = async () => {
//     if (!username || !password) {
//       setError('Please enter both username and password');
//       return; // Exit early if fields are empty
//     }

//     const userData = { username, password };

//     try {
//       const token = await APIService.login(userData.username, userData.password);

//       setToken('mytoken', token);
//       navigate('/categories');
//     } catch (error) {
//       setError('Incorrect username or password');
//       console.error('Login error:', error);
//     }
//   };

//   // Register button click handler
//   const registerBtn = async () => {
//     if (!username || !password) {
//       setError('Please enter both username and password');
//       return; // Exit early if fields are empty
//     }

//     const userData = { username, password };

//     try {
//       await APIService.createUser(userData.username, userData.password);
//       alert('User successfully created!');
//       console.log('User successfully created:', username);

//       // Clear input fields and navigate
//       setUserName('');
//       setPassword('');
//       setError('');
//       navigate('/categories');
//     } catch (error) {
//       setError('Error creating user');
//       console.error('Error creating user:', error);
//     }
//   };

//   // JSX rendering
//   return (
//     <div
//       className='container d-flex justify-content-center align-items-center'
//       style={{ minHeight: '100vh', }} 
//     >
//        {/* backgroundColor: '#50a3a2' */}
//       <div className='col-md-4'>
//         <form className='form-signin'>
//           <h1 className='h3 mb-3 fw-normal'>{isLogin ? 'Login' : 'Register'}</h1>

//           {error && <div className='alert alert-danger'>{error}</div>}

//           <div className='form-floating'>
//             <input
//               type='text'
//               className='form-control'
//               id='username'
//               placeholder='Please enter username'
//               value={username}
//               onChange={(e) => setUserName(e.target.value)}
//             />
//             <label htmlFor='username'>Username</label>
//           </div>

//           <div className='form-floating'>
//             <input
//               type='password'
//               className='form-control'
//               id='password'
//               placeholder='Password'
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//             />
//             <label htmlFor='password'>Password</label>
//           </div>

//           <button
//             className='w-100 btn btn-lg btn-primary'
//             type='button'
//             onClick={isLogin ? loginBtn : registerBtn}
//           >
//             {isLogin ? 'Login' : 'Register'}
//           </button>

//           <div className='mt-3'>
//             {isLogin ? (
//               <p>
//                 Don't have an account?{' '}
//                 <button className='btn btn-link' onClick={() => setLogin(false)}>
//                   Sign up
//                 </button>
//               </p>
//             ) : (
//               <p>
//                 Already have an account?{' '}
//                 <button className='btn btn-link' onClick={() => setLogin(true)}>
//                   Login
//                 </button>
//               </p>
//             )}
//           </div>
//         </form>
//       </div>
//     </div>
//   );
// }

// export default Login;


// import React, { useState, useEffect } from 'react';
// import APIService from '../APIService';
// import { useCookies } from 'react-cookie';
// import { useNavigate } from 'react-router-dom';

// function Login() {
//   // State variables
//   const [username, setUserName] = useState('');
//   const [password, setPassword] = useState('');
//   const [isLogin, setLogin] = useState(true);
//   const [token, setToken] = useCookies(['mytoken']);
//   const [error, setError] = useState('');
//   const navigate = useNavigate();

//   // Effect to check for token and redirect if present
//   useEffect(() => {
//     if (token['mytoken']) {
//       navigate('/categories');
//     }
//   }, [token, navigate]);

//   // Login button click handler
//   const loginBtn = async () => {
//     if (!username || !password) {
//       setError('Please enter both username and password');
//       return; // Exit early if fields are empty
//     }

//     const userData = { username, password };

//     try {
//       const token = await APIService.login(userData.username, userData.password);

//       setToken('mytoken', token);
//       navigate('/categories');
//     } catch (error) {
//       setError('Incorrect username or password');
//       console.error('Login error:', error);
//     }
//   };

//   // Register button click handler
//   const registerBtn = async () => {
//     if (!username || !password) {
//       setError('Please enter both username and password');
//       return; // Exit early if fields are empty
//     }

//     const userData = { username, password };

//     try {
//       await APIService.createUser(userData.username, userData.password);
//       alert('User successfully created!');
//       console.log('User successfully created:', username);

//       // Clear input fields and navigate
//       setUserName('');
//       setPassword('');
//       setError('');
//       navigate('/categories');
//     } catch (error) {
//       setError('Error creating user');
//       console.error('Error creating user:', error);
//     }
//   };

//   // JSX rendering
//   return (
//     <div className='App'>
//       <br />
//       <br />
//       {isLogin ? <h1>Login</h1> : <h1>Register</h1>}
//       <br />
//       <br />
//       {error && <div className='alert alert-danger'>{error}</div>}
//       <div className='mb-3'>
//         <label htmlFor='username' className='form-label'>
//           Username
//         </label>
//         <input
//           type='text'
//           className='form-control'
//           id='username'
//           placeholder='Please enter username'
//           value={username}
//           onChange={(e) => setUserName(e.target.value)}
//         />
//       </div>

//       <div className='mb-3'>
//         <label htmlFor='password' className='form-label'>
//           Password
//         </label>
//         <input
//           type='password'
//           className='form-control'
//           id='password'
//           placeholder='Password'
//           value={password}
//           onChange={(e) => setPassword(e.target.value)}
//         />
//       </div>

//       <button onClick={isLogin ? loginBtn : registerBtn} className='btn btn-primary'>
//         {isLogin ? 'Login' : 'Register'}
//       </button>
//       <div className='mb-3'>
//         <br />
//         {isLogin ? (
//           <h5>
//             You don't have an account, please{' '}
//             <button className='btn btn-primary' onClick={() => setLogin(false)}>
//               Sign up
//             </button>{' '}
//             here
//           </h5>
//         ) : (
//           <h5>
//             If you have an account,{' '}
//             <button className='btn btn-primary' onClick={() => setLogin(true)}>
//               Login
//             </button>{' '}
//             here
//           </h5>
//         )}
//       </div>
//     </div>
//   );
// }

// export default Login;

























import React, { useState, useEffect } from 'react';
import APIService from '../APIService';
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router-dom';

function Login() {
  // State variables
  const [username, setUserName] = useState('');
  const [password, setPassword] = useState('');
  const [isLogin, setLogin] = useState(true);
  const [token, setToken] = useCookies(['mytoken']);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Effect to check for token and redirect if present
  useEffect(() => {
    if (token['mytoken']) {
      navigate('/categories');
    }
  }, [token, navigate]);

  // Login button click handler
  const loginBtn = async () => {
    if (!username || !password) {
      setError('Please enter both username and password');
      return; // Exit early if fields are empty
    }

    const userData = { username, password };

    try {
      const token = await APIService.login(userData.username, userData.password);

      setToken('mytoken', token);
      navigate('/categories');
    } catch (error) {
      setError('Incorrect username or password');
      console.error('Login error:', error);
    }
  };

  // Register button click handler
  const registerBtn = async () => {
    if (!username || !password) {
      setError('Please enter both username and password');
      return; // Exit early if fields are empty
    }

    const userData = { username, password };

    try {
      await APIService.createUser(userData.username, userData.password);
      alert('User successfully created!');
      console.log('User successfully created:', username);

      // Clear input fields and navigate
      setUserName('');
      setPassword('');
      setError('');
      navigate('/categories');
    } catch (error) {
      setError('Error creating user');
      console.error('Error creating user:', error);
    }
  };

  // JSX rendering
  return (
    <div className='App text-center'>
      <div className='d-flex justify-content-center align-items-center vh-100'>
        <div>
          <br />
          <br />
          {isLogin ? <h1>Login</h1> : <h1>Register</h1>}
          <br />
          <br />
          {error && <div className='alert alert-danger'>{error}</div>}
          <div className='mb-3'>
            <label htmlFor='username' className='form-label'>
              Username
            </label>
            <input
              type='text'
              className='form-control'
              id='username'
              placeholder='Please enter username'
              value={username}
              onChange={(e) => setUserName(e.target.value)}
            />
          </div>

          <div className='mb-3'>
            <label htmlFor='password' className='form-label'>
              Password
            </label>
            <input
              type='password'
              className='form-control'
              id='password'
              placeholder='Password'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button onClick={isLogin ? loginBtn : registerBtn} className='btn btn-primary'>
            {isLogin ? 'Login' : 'Register'}
          </button>
          <div className='mb-3'>
            <br />
            {isLogin ? (
              <h5>
                You don't have an account, please{' '}
                <button className='btn btn-primary' onClick={() => setLogin(false)}>
                  Sign up
                </button>{' '}
                here
              </h5>
            ) : (
              <h5>
                If you have an account,{' '}
                <button className='btn btn-primary' onClick={() => setLogin(true)}>
                  Login
                </button>{' '}
                here
              </h5>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
