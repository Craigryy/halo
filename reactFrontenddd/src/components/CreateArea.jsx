import React, { useState, useEffect } from 'react';
import APIService from '../APIService';
import { useCookies } from 'react-cookie';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit, faPlus, faTrash } from '@fortawesome/free-solid-svg-icons';
import '../CreateArea.css';

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
    if (props.category) {
      setName(props.category.name || '');
      setCreatedBy(props.category.created_by || '');
    }
  }, [props.category]);

  useEffect(() => {
    if (props.book) {
      setBookTitle(props.book.title || '');
      setBookAuthor(props.book.author || '');
      setBookCategory(props.book.category_id || '');
    }
  }, [props.book]);


  useEffect(() => {
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
  
    fetchCategories();
  }, [token]);
  

  const updateCategory = () => {
    APIService.UpdateCategory(props.category.id, { name, created_by }, token['mytoken'])
      .then(updatedCategory => {
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

    APIService.updateBook(props.book.category_id, props.book.id, updatedBookData, token['mytoken'])
      .then(updatedBook => {
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

  const insertCategory = () => {
    APIService.insertCategory({ name, created_by }, token['mytoken'])
      .then(resp => {
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

  const handleCloseForms = () => {
    setShowBookForm(false);
    setName('');
    setCreatedBy('');
    setBookTitle('');
    setBookAuthor('');
    setBookCategory('');
    setError(null);
  };

  const handleCloseBookForm = () => {
    setShowBookForm(false);
    setBookTitle('');
    setBookAuthor('');
    setBookCategory('');
    setError(null);
  };

  const handleAddBook = () => {
    setShowBookForm(true);
  };

  return (
    <div className="create-area-container">
      {props.category && (
        <div className="form-container">
          {/* Category Form */}
          <div className="form-section">
            <h3>Category Form</h3>
            <label htmlFor="name" className="form-label">
              Name of Category
            </label>
            <input
              type="text"
              className="form-control"
              name="name"
              placeholder="Please enter name of the category "
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
              <button onClick={updateCategory} className="btn btn-success">
                <FontAwesomeIcon icon={faEdit} /> Update category
              </button>
            ) : (
              <button onClick={insertCategory} className="btn btn-success">
                <FontAwesomeIcon icon={faPlus} /> Insert category
              </button>
            )}
          </div>

          {/* Book Form */}
          <div className="form-section">
            {showBookForm && (
              <div>
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
                  <button onClick={updateBook} className="btn btn-success">
                    <FontAwesomeIcon icon={faEdit} /> Update book
                  </button>
                ) : (
                  <button onClick={handleBookSubmit} className="btn btn-success">
                    <FontAwesomeIcon icon={faPlus} /> Add book
                  </button>
                )}
              </div>
            )}

            {!showBookForm && (
              <div>
                <button onClick={handleAddBook} className="btn btn-primary">
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
