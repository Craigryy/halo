import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import CategoryList from '../components/categoryList';

describe('CategoryList', () => {
  it('renders a mock category and mock book', () => {
    const mockCategory = {
      id: 1,
      name: 'Fiction',
      created_by: 'User1',
    };

    const mockBook = {
      id: 1,
      title: 'Book1',
      author: 'Author1',
      category_id: 1,
    };

    const { getByText, getByLabelText } = render(
      <CategoryList
        categories={[mockCategory]}
        books={[mockBook]}
        showBooks={{ 1: false }} // Set showBooks to false initially
        // Mock other props as needed
      />
    );

    // Check if mock category name is rendered
    const categoryElement = getByText(mockCategory.name);
    expect(categoryElement).toBeInTheDocument();

    // Check if "Update" and "Delete" buttons are rendered for mock category
    const updateButton = getByText('Update');
    expect(updateButton).toBeInTheDocument();

    const deleteButton = getByText('Delete');
    expect(deleteButton).toBeInTheDocument();

    // Click on the categwory header to toggle visibility of books
    fireEvent.click(categoryElement);

  });

  });

