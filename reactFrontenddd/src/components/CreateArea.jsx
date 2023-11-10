import React, { useState, useEffect } from 'react';
import APIService from '../APIService';
import { useCookies } from 'react-cookie';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit, faPlus, faTimes } from '@fortawesome/free-solid-svg-icons';
import '../CSS/CreateArea.css';


/**
 *  CreateArea component.
 *
 * @function
 * @returns {JSX.Element} The rendered JSX element.
 */

function CreateArea(props) {
  const [name, setName] = useState('');
  const [created_by, setCreatedBy] = useState('');
  const [title, setBookTitle] = useState('');
  const [author, setBookAuthor] = useState('');
  const [category_id, setBookCategory] = useState('');
  const [token] = useCookies(['mytoken']);
  const [error, setError] = useState(null);
  const [showBookForm, setShowBookForm] = useState(false);
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    /**
     * Sets the component state based on the category prop.
     * If a category prop is provided, updates the name and created_by state.
     *
     * @function
     * @returns {void}
     */
    const setCategoryStateFromProps = () => {
      if (props.category) {
        setName(props.category.name || '');
        setCreatedBy(props.category.created_by || '');
      }
    };
  
    // Call the setCategoryStateFromProps function when the category prop changes
    setCategoryStateFromProps();
  }, [props.category]);
  

  useEffect(() => {
    /**
     * Sets the component state based on the book prop.
     * If a book prop is provided, updates the title, author, and category state.
     *
     * @function
     * @returns {void}
     */
    const setBookStateFromProps = () => {
      if (props.book) {
        setBookTitle(props.book.title || '');
        setBookAuthor(props.book.author || '');
        setBookCategory(props.book.category_id || '');
      }
    };
  
    // Call the setBookStateFromProps function when the book prop changes
    setBookStateFromProps();
  }, [props.book]);
  

  useEffect(() => {
    /**
     * Fetches categories from the API and updates the component state.
     *
     * @function
     * @async
     * @returns {void}
     */
    const fetchCategories = async () => {
      try {
        const response = await APIService.makeRequest('/categories', 'GET', null, token['mytoken']);
        if (Array.isArray(response)) {
          setCategories(response);
        } else {
          console.error('Error fetching categories:', response);
        }
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };
  
    // Call the fetchCategories function when the component mounts or when the token changes
    fetchCategories();
  }, [token]);
  

/**
 * Updates an existing category with new information.
 *
 * @function
 * @returns {void}
 */
const updateCategory = () => {
  APIService.UpdateCategory(props.category.id, { name, created_by }, token['mytoken'])
    .then(updatedCategory => {
      // Updates the state with the updated category information
      props.updatedInformation(updatedCategory);
      setName('');
      setCreatedBy('');
      setError(null);
    })
    .catch(error => {
      console.error('Error updating category:', error);
      setError('Error updating category. Please try again.');
    });
};


/**
 * Updates an existing book with new information or adds a new book if no book ID is provided.
 * Validates the book details and calls the API to update/add the book.
 *
 * @function
 * @returns {void}
 */
const updateBook = () => {
  if (!title || !author || !category_id) {
    setError('Please fill in all book details.');
    return;
  }

  const updatedBookData = {
    title: title,
    author: author,
    category_id: category_id,
  };

  // Calls the API to update/add the book
  APIService.updateBook(category_id, props.book?.id, updatedBookData, token['mytoken'])
    .then(updatedBook => {
      // Updates the state with the updated book information
      props.updatedBookInformation(updatedBook);
      setBookAuthor('');
      setBookTitle('');
      setBookCategory('');
      setError(null);
    })
    .catch(error => {
      console.error('Error updating book:', error);
      setError('Error updating book. Please try again.');
    });
};


/**
 * Inserts a new category using the provided name and creator, calling the API for insertion.
 * After successful insertion, updates the component state and resets form-related state values.
 *
 * @function
 * @returns {void}
 */
const insertCategory = () => {
  APIService.insertCategory({ name, created_by }, token['mytoken'])
    .then(resp => {
      // Updates the state with the inserted category information
      props.insertedInformation(resp);
      setName('');
      setCreatedBy('');
      setError(null);
    })
    .catch(error => {
      console.error('Error inserting category:', error);
      setError('Error inserting category. Please try again.');
    });
};


  /**
  * Handles the submission of book information to be added to the system.
  * Validates the book details and calls the API to add the book.

  * @function
  * @returns {void}
  */
  const handleBookSubmit = () => {
    if (!title || !author || !category_id) {
      setError('Please fill in all book details.');
      return;
    }

    const bookData = {
      title: title,
      author: author,
      category_id: category_id,
    };

    APIService.addBook(category_id, bookData, token['mytoken'])
      .then(resp => {
        props.insertedBookInformation(resp);
        setBookAuthor('');
        setBookCategory('');
        setBookTitle('');
        setError(null);
      })
      .catch(error => {
        console.error('Error adding book:', error);
        setError('Error adding book. Please try again.');
      });
  };

/**
 * Resets form-related state values and hides the book form.
 *
 * @function
 * @returns {void}
 */
const handleCloseForms = () => {
  setShowBookForm(false);
  setName('');
  setCreatedBy('');
  setBookTitle('');
  setBookAuthor('');
  setBookCategory('');
  setError(null);
};


 /**
 * Sets the book form visibility to true, enabling the addition of a new book.
 *
 * @function
 * @returns {void}
 */
const handleAddBook = () => {
  setShowBookForm(true);
};


  return (
    <div className="create-area-container">
      <button
          className="btn btn-success"
          style={{ backgroundColor: '#F6F5F5', border: '2px solid #99C8F2', marginLeft: '5px', color: '#99C8F2', float: 'right', transition: 'opacity 0.5s' }}
          onClick={props.closeCreateArea}
        >
          <FontAwesomeIcon icon={faTimes} style={{ backgroundColor: '#FFFAFA' }} />
          CLOSE
        </button>
      {props.category && (
        <div className="form-container">
          <div className="form-section">
            <h3>Category Form</h3>
            <label htmlFor="name" className="form-label">
              Name of Category
            </label>
            <input
              type="text"
              className="form-control"
              name="name"
              placeholder="Please enter name of the category"
              value={name}
              onChange={e => setName(e.target.value)}
            />
            <label htmlFor="created_by" className="form-label">
              Created by
            </label>
            <input
              type="text"
              className="form-control"
              name="created_by"
              placeholder="Please enter the creator"
              value={created_by}
              onChange={e => setCreatedBy(e.target.value)}
            />
            {props.category.id ? (
              <button onClick={updateCategory} className="btn button1">
                <FontAwesomeIcon icon={faEdit} /> Update category
              </button>
            ) : (
              <button onClick={insertCategory} className="btn button2">
                <FontAwesomeIcon icon={faPlus} /> Insert category
              </button>
            )}
          </div>

          <div className="form-section">
            {showBookForm && (
              <div>
                <br />
                <h3>Book Form</h3>
                <label htmlFor="bookTitle" className="form-label">
                  Title
                </label>
                <input
                  type="text"
                  className="form-control"
                  name="bookTitle"
                  placeholder="Enter title"
                  value={title}
                  onChange={e => setBookTitle(e.target.value)}
                />
                <label htmlFor="bookAuthor" className="form-label">
                  Author
                </label>
                <input
                  type="text"
                  className="form-control"
                  name="bookAuthor"
                  placeholder="Enter author"
                  value={author}
                  onChange={e => setBookAuthor(e.target.value)}
                />
                <label htmlFor="bookCategory" className="form-label">
                  Category
                </label>
                <select
                  className="form-control"
                  name="bookCategory"
                  value={category_id}
                  onChange={e => setBookCategory(e.target.value)}
                >
                  <option value="">Select a category</option>
                  {categories.map(category => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
                </select>
                {props.book && props.book.id ? (
                  <button onClick={updateBook} className="btn button2">
                    <FontAwesomeIcon icon={faEdit} /> Update book
                  </button>
                ) : (
                  <button onClick={handleBookSubmit} className="btn button2">
                    <FontAwesomeIcon icon={faPlus} /> Add book
                  </button>
                )}
              </div>
            )}
            <br />

            {!showBookForm && (
              <div>
                <button onClick={handleAddBook} className="btn button1">
                  <FontAwesomeIcon icon={faPlus} /> Add Book
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {error && <p className="text-danger">{error}</p>}
    </div>
  );
}

export default CreateArea;
