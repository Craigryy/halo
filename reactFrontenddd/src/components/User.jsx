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
  const [isConfirmationVisible, setIsConfirmationVisible] = useState(false);
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

  // Function to handle user deletion with confirmation
  const handleDeleteUser = (user) => {
    // Show the confirmation dialog
    setIsConfirmationVisible(true);
  };

  // Function to handle confirmation button click
  const handleConfirmation = () => {
    // Check if the access code is correct
    if (accessCode === 'jamesharrison') {
      setIsConfirmationVisible(false);
      // Continue with user deletion
      APIService.deleteUser(selectedUser.id, token['mytoken'])
        .then(() => {
          // Fetch the updated list of users after successful deletion
          setAccessCode('');
          fetchAllUsers();
          // Call the parent component's deleteBtnUser function
          deleteBtnUser(selectedUser);
        })
        .catch((error) => {
          console.error('Error deleting user:', error);
        });
    } else {
      // Display an error message for incorrect access code
      setError('Wrong access code. Please try again.');
    }
  };

  // Function to hide users
  const handleHideUsers = () => {
    setShowUsers(false);
  };

  // Selected user for deletion
  const [selectedUser, setSelectedUser] = useState(null);

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
                <button onClick={() => {
                  setSelectedUser(user);
                  handleDeleteUser(user);
                }}>Delete</button>
              </li>
            ))}
          </ul>
        </div>
      )}
      {/* Confirmation Modal */}
      {isConfirmationVisible && (
        <div className="confirmation-modal">
          <p>Enter access code to confirm:</p>
          <input
            type="password"
            value={accessCode}
            onChange={(e) => setAccessCode(e.target.value)}
          />
          <button onClick={handleConfirmation}>Confirm</button>
        </div>
      )}
    </div>
  );
}

export default User;
