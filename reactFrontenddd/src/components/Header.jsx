import React from 'react';
import '../CSS/header.css';

function Header(props) {
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
