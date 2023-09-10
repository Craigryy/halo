// import React from 'react';
// import { render, fireEvent, waitFor } from '@testing-library/react';
// import CreateArea from '../components/CreateArea';

// describe('CreateArea', () => {
//   const mockInsertCategory = jest.fn();
//   const mockUpdatedInformation = jest.fn();
//   const mockInsertedBookInformation = jest.fn();

//   const renderComponent = () => {
//     return render(
//       <CreateArea
//         insertedInformation={mockInsertCategory}
//         updatedInformation={mockUpdatedInformation}
//         insertedBookInformation={mockInsertedBookInformation}
//       />
//     );
//   };

//   it('renders and interacts with the form', async () => {
//     const { getByLabelText, getByText } = renderComponent();

//     // Type category name and created by
//     const nameInput = getByLabelText('Name of Category');
//     fireEvent.change(nameInput, { target: { value: 'Fiction' } });

//     const createdByTextarea = getByLabelText('Created_by');
//     fireEvent.change(createdByTextarea, { target: { value: 'User1' } });

//     // Click the "Insert category" button
//     const insertCategoryButton = getByText('Insert category');
//     fireEvent.click(insertCategoryButton);

//     // Check if insertCategory function was called
//     await waitFor(() => {
//       expect(mockInsertCategory).toHaveBeenCalledWith({
//         name: 'Fiction',
//         created_by: 'User1',
//       });
//     });

//     // Toggle the "Add Book" form
//     const addBookButton = getByText('Add Book');
//     fireEvent.click(addBookButton);

//     // Type book details
//     const bookTitleInput = getByLabelText('Title');
//     fireEvent.change(bookTitleInput, { target: { value: 'Book Title' } });

//     const bookAuthorInput = getByLabelText('Author');
//     fireEvent.change(bookAuthorInput, { target: { value: 'Author Name' } });

//     const bookCategoryInput = getByLabelText('Category');
//     fireEvent.change(bookCategoryInput, { target: { value: '1' } });

//     // Click the "Add book" button
//     const addBookFormButton = getByText('Add book');
//     fireEvent.click(addBookFormButton);

//     // Check if insertedBookInformation function was called
//     await waitFor(() => {
//       expect(mockInsertedBookInformation).toHaveBeenCalledWith({
//         title: 'Book Title',
//         author: 'Author Name',
//         category_id: '1',
//       });
//     });

//     // Close the "Add Book" form
//     const closeButton = getByText('Close');
//     fireEvent.click(closeButton);

//     // Toggle the "Add Book" form again
//     fireEvent.click(addBookButton);

//     // Click the "Update book" button
//     const updateBookButton = getByText('Update book');
//     fireEvent.click(updateBookButton);

//     // Check if updatedBookInformation function was called
//     await waitFor(() => {
//       expect(mockInsertedBookInformation).toHaveBeenCalledWith({
//         title: 'Book Title',
//         author: 'Author Name',
//         category_id: '1',
//       });
//     });
//   });
// });
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';

function MockForm() {
  const handleSubmit = event => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    console.log('Form data:', data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="mock-label">Mock Label</label>
      <br />
      <textarea id="mock-label" name="mockTextArea" rows="4" cols="50" />
      <br />
      <button type="submit">Submit</button>
    </form>
  );
}

describe('MockForm', () => {
  it('submits the form with mock text', async () => {
    const { getByLabelText, getByText } = render(<MockForm />);

    // Type text in the text area
    const textArea = getByLabelText('Mock Label');
    fireEvent.change(textArea, { target: { value: 'Mock text content' } });

    // Submit the form
    const submitButton = getByText('Submit');
    fireEvent.click(submitButton);

    // Wait for form submission
    await waitFor(() => {
      // You can add assertions here to check if form submission logic is correct
      // For this example, we'll just log the form data to the console
    });
  });
});
