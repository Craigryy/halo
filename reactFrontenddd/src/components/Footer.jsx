import React from "react";

/**
 * Footer component displaying the copyright year.
 *
 * @component
 * @returns {JSX.Element} Footer component JSX
 */
function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer>
      <p>Copyright ⓒ {year}</p>
    </footer>
  );
}

export default Footer;
