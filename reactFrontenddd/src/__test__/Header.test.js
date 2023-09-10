import React from 'react';
import { render, screen } from '@testing-library/react';
import Header from '../components/Header';

describe('Header component', () => {
  it('renders the header title', () => {
    const title = 'My Header Title';
    render(<Header title={title} />);
    
    const headerTitle = screen.getByText(title);
    expect(headerTitle).toBeInTheDocument();
  });
  
  // Add more test cases as needed
});
