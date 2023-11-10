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
    });
  });
});
