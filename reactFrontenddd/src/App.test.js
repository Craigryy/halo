import React from 'react';
import { render } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom'; // Import MemoryRouter
import App from './App';

test('renders app component', () => {
  const { getByText } = render(
    // Wrap your component with MemoryRouter
    <MemoryRouter>
      <App />
    </MemoryRouter>
  );

  // Test that the title is rendered
  const titleElement = getByText(/Halo/i);
  expect(titleElement).toBeInTheDocument();

  // Test that the "INSERT" button is rendered
  const insertButtonElement = getByText(/INSERT/i);
  expect(insertButtonElement).toBeInTheDocument();

  // Test that the "Logout" button is rendered
  const logoutButtonElement = getByText(/Logout/i);
  expect(logoutButtonElement).toBeInTheDocument();
});
