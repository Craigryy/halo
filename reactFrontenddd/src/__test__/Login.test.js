import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import Login from '../components/login';
import APIService from '../APIService';

jest.mock('../APIService');

describe('Login component', () => {
  // ... other tests ...

  test('calls the registration function and displays a success message on successful registration', async () => {
    APIService.createUser.mockResolvedValue({ success: true });

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    const signUpLink = screen.getByText(/Sign up/i);
    fireEvent.click(signUpLink);

    const usernameInput = screen.getByPlaceholderText(/Please enter username/i);
    const passwordInput = screen.getByPlaceholderText(/Password/i);
    const registerButton = screen.getByRole('button', { name: /Register/i });

    userEvent.type(usernameInput, 'newuser');
    userEvent.type(passwordInput, 'newpassword');
    fireEvent.click(registerButton);

    
  });

  
});
