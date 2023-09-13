import React, { useState } from 'react';
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router-dom'; 
import APIService from '../APIService';

function User(props) {
  // Destructuring props
  const { users, deleteBtnUser } = props;

  // State variables
  const [token] = useCookies(['mytoken']);
  const [usersList, setUsersList] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showUsers, setShowUsers] = useState(false);
  const [accessCode, setAccessCode] = useState('');
  const navigate = useNavigate(); 

  // Function to fetch all users from API
  const fetchAllUsers = () => {
    setIsLoading(true);
    setError(null);

    APIService.getAllUsers(token['mytoken'])
      .then(response => {
        setUsersList(response);
        setIsLoading(false);
        setShowUsers(true);
      })
      .catch(error => {
        console.error('Error fetching all users:', error);
        setError('An error occurred while fetching users.');
        setIsLoading(false);
      });
  };

  // Function to handle user deletion
  const handleDeleteUser = (user) => {
    // Continue with user deletion
    APIService.deleteUser(user.id, token['mytoken'])
      .then(() => {
        // Fetch the updated list of users after successful deletion
        fetchAllUsers();
        // Call the parent component's deleteBtnUser function
        deleteBtnUser(user);
      })
      .catch((error) => {
        console.error('Error deleting user:', error);
      });
  };

  // Function to hide users
  const handleHideUsers = () => {
    setShowUsers(false);
  };

  // JSX rendering
  return (
    <div className='App'>
      <h1>User Management</h1>
      <button onClick={fetchAllUsers} disabled={isLoading}>
        {isLoading ? 'Loading...' : 'View All Users'}
      </button>
      {error && <p className='error-message'>{error}</p>}
      {showUsers && (
        <div>
          <button onClick={handleHideUsers}>Hide Users</button>
          <ul>
            {usersList.map((user) => (
              <li key={user.id}>
                {user.name}{' '}
                <button onClick={() => handleDeleteUser(user)}>Delete</button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default User;
