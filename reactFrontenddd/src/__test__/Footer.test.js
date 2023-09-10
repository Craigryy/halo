import React from 'react';
import { render, screen } from '@testing-library/react';
import Footer from '../components/Footer'; // Adjust the path according to your project structure

test('renders footer with current year', () => {
  render(<Footer />);

  const currentYear = new Date().getFullYear();
  const copyrightText = screen.getByText(`Copyright ⓒ ${currentYear}`);

  expect(copyrightText).toBeInTheDocument();
});
