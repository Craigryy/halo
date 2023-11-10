import React from 'react';
import '../CSS/header.css';

/**
 * Header component displaying the application logo and logout button.
 *
 * @component
 * @param {object} props - The properties passed down to the component.
 * @param {Function} props.logoutBtn - Function to handle the logout action.
 * @returns {JSX.Element} Header component JSX
 */
function Header(props) {
  /**
   * Handles the logout action by calling the provided logoutBtn function.
   *
   * @function
   * @returns {void}
   */
  const handleLogout = () => {
    props.logoutBtn();
  };

  return (
    <div className="header-container">
      <a href="/">
        <img id="logo_img" src="https://cdn.anotepad.com/images/anotepad.svg" alt="aNotepad" />
        <span id="title">Halo</span>
      </a>
      <ul className="header-list">
        <li className="header-list-item">
          <a onClick={handleLogout} style={{ color: '#fff', textDecoration: 'none', cursor: 'pointer' }}>Logout</a>
        </li>
      </ul>
    </div>
  );
}

export default Header;
