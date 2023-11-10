import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { useNavigate } from 'react-router-dom';
import { useCookies } from 'react-cookie';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';

import './App.css';

import APIService from './APIService';
import CategoryList from './components/categoryList';
import CreateArea from './components/CreateArea';
import Header from './components/Header';
import Footer from './components/Footer';
import Login from './components/login';

/**
 * Main application component.
 *
 * @function
 * @returns {JSX.Element} The rendered JSX element.
 */
function App() {
  const [categories, setCategories] = useState([]);
  const [token, setToken, removeCookie] = useCookies(['mytoken']);
  const navigate = useNavigate();
  const [books, setBooks] = useState([]);
  const [editedCategory, setEditedCategory] = useState(null);
  const [editedBook, setEditedBook] = useState(null);
  const [showBooks, setShowBooks] = useState({});
  const [editedCategories, setEditedCategories] = useState(null);

  useEffect(() => {
    /**
     * Fetches categories from the API.
     *
     * @function
     * @async
     * @returns {void}
     * @param {string} url - The API endpoint URL.
     * @param {string} method - The HTTP request method (e.g., 'GET').
     * @param {object|null} data - Optional data to send with the request.
     * @param {string} authToken - The authentication token.
     * @returns {Promise<any>} A Promise that resolves with the response data.
     * @throws {Error} If the API request fails.
     */
    const fetchCategories = async () => {
      try {
        const resp = await APIService.makeRequest('/categories/', 'GET', null, token['mytoken']);
        setCategories(resp);
      } catch (error) {
        console.log(error);
      }
    };

    fetchCategories();
  }, [token]);


  useEffect(() => {
    /**
     * Fetches books from the API.
     *
     * @function
     * @async
     * @returns {void}
     * @param {string} url - The API endpoint URL.
     * @param {string} method - The HTTP request method (e.g., 'GET').
     * @param {object|null} data - Optional data to send with the request.
     * @param {string} authToken - The authentication token.
     * @returns {Promise<any>} A Promise that resolves with the response data.
     * @throws {Error} If the API request fails.
     */
    const fetchBooks = async () => {
      try {
        const resp = await APIService.makeRequest('/books/', 'GET', null, token['mytoken']);
        setBooks(resp);
      } catch (error) {
        console.log(error);
      }
    };

    fetchBooks();
  }, [token]);


  useEffect(() => {
    /**
     * Checks if a valid token is present and navigates to the login page if not.
     *
     * @function
     * @param {string} authToken - The authentication token.
     * @returns {Promise<void>} A Promise that resolves after fetching .
     */
    const checkToken = () => {
      if (!token['mytoken']) {
        // Navigates to the login page if the authentication token is not present.
        navigate('/');
      }
    };
  
    // Invokes the checkToken function.
    checkToken();
  }, [token, navigate]);
  

  /**
 * Edits a category by setting it as the edited category for further actions.
 *
 * @function
 * @param {Object} category - The category to edit.
 * @returns {void}
 */
  const editCat = category => {
    setEditedCategories(category);
  };


  /**
   * Edits a category book.
   *
   * @function
   * @param {Object} book - The book to edit.
   *  @returns {void}
   */
  const editCatBook = book => {
    setEditedBook(book);
  };


 /**
 * Fetches categories from the API and sets them in the component state.
 *
 * @function
 * @async
 * @param {string} url - The API endpoint URL (e.g,'/categories/).
 * @param {string} method - The HTTP request method (e.g., 'GET').
  * @param {object|null} data - Optional data to send with the request.
  * @param {string} authToken - The authentication token.
  * @returns {Promise<any>} A Promise that resolves with the response data.
 */
const fetchCategories = async () => {
  try {
    const resp = await APIService.makeRequest('/categories/', 'GET', null, token['mytoken']);
    setCategories(resp);
  } catch (error) {
    console.error('Error fetching categories:', error);
  }
};


  /**
   * Fetches books from the API.
   *
   * @function
   * @async
    * @param {string} url - The API endpoint URL (e.g,'/books/).
    * @param {string} method - The HTTP request method (e.g., 'GET').
   */
  const fetchBooks = async () => {
    try {
      const resp = await APIService.makeRequest('/books/', 'GET', null, token['mytoken']);
      setBooks(resp);
    } catch (error) {
      console.log(error);
    }
  };

  /**
   * Updates category information.
   *
   * @function
   * @param {Object} category - The updated category.
   */
  const updatedInformation = category => {
    const new_categories = categories.map(mycategory => {
      if (mycategory.id === category.id) {
        return category;
      } else {
        return mycategory;
      }
    });
    setCategories(new_categories);
    fetchCategories();
  };

  /**
   * Updates book information.
   *
   * @function
   * @param {Object} book - The updated book.
   */
  const updatedBookInformation = book => {
    const new_books = books.map(mybook => {
      if (mybook.id === book.id) {
        return book;
      } else {
        return mybook;
      }
    });
    setBooks(new_books);
    fetchCategories();
    fetchBooks();
  };

  /**
   * Inserts category information.
   *
   * @function
   * @param {Object} category - The inserted category.
   */
  const insertedInformation = category => {
    const new_categories = [...categories, category];
    setCategories(new_categories);
    setEditedCategories(null);
    fetchCategories();
    fetchBooks();
  };

  /**
   * Deletes a category.
   *
   * @function
   * @param {Object} category - The category to delete.
   */
  const deleteBtn = category => {
    const new_category = categories.filter(mycategory => mycategory.id !== category.id);
    setCategories(new_category);
    fetchCategories();
    fetchBooks();
  };

  /**
   * Logs out the user.
   *
   * @function
   * @param {string} authToken - The authentication token.
   */
  const logoutBtn = () => {
    removeCookie('mytoken');
    navigate('/');
  };

  /**
   * Deletes a book.
   *
   * @function
   * @param {Object} book - The book to delete.
   */
  const deleteBtnBook = book => {
    const new_Books = books.filter(myBooks => myBooks.id !== book.id);
    setBooks(new_Books);
    fetchBooks();
    fetchCategories();
  };

  /**
   * Handles editing of a category.
   *
   * @function
   * @param {Object} category - The category to edit.
   */
  const handleEditCategory = category => {
    setEditedCategory(category);
  };

  /**
   * Handles editing of a book.
   *
   * @function
   * @param {Object} book - The book to edit.
   */
  const handleEditBook = book => {
    setEditedBook(book);
  };

  /**
   * Toggles the display of books in a category.
   *
   * @function
   * @param {string} categoryId - The ID of the category to toggle.
   */
  const toggleShowBooks = categoryId => {
    setShowBooks(prevShowBooks => ({
      ...prevShowBooks,
      [categoryId]: !prevShowBooks[categoryId],
    }));
  };

  /**
   * Opens the create area for a category.
   *
   * @function
   */
  const openCreateArea = () => {
    setEditedCategory({ name: '', created_by: '' });
  };

  /**
   * Closes the create area for a category.
   *
   * @function
   * @returns {void}
   */
  const closeCreateArea = () => {
    setEditedCategory(null);
  };


/**
 * Inserts book information and updates the component state accordingly.
 *
 * @function
 * @param {Object} book - The inserted book.
 * @returns {void}
 */
const insertedBookInformation = book => {
  const new_books = [...books, book];
  setBooks(new_books);
  setEditedBook(null); // Reset the edited book
  fetchCategories();
  fetchBooks();
};


  return (
    <div className="App">
      <div className="row">
        <div className="col">
          <Header logoutBtn={logoutBtn} />
        </div>
      </div>
      <br />
      <br />
      <CategoryList
        categories={categories}
        books={books}
        showBooks={showBooks}
        toggleShowBooks={toggleShowBooks}
        editCat={handleEditCategory}
        editCatBook={handleEditBook}
        deleteBtn={deleteBtn}
        deleteBtnBook={deleteBtnBook}
      />
      <br />
      <button
        className="btn btn-success"
        style={{ backgroundColor: '#F6F5F5', border: '2px solid #D92929', color: '#D92929', float: 'left' }}
        onClick={openCreateArea}
      >
        <FontAwesomeIcon icon={faPlus} style={{ backgroundColor: '#FFFAFA' }} />
        INSERT
      </button>
      <br />

      {editedCategory || editedBook ? (
        <CreateArea
          category={editedCategory}
          book={editedBook}
          updatedInformation={updatedInformation}
          insertedInformation={insertedInformation}
          insertedBookInformation={insertedBookInformation}
          updatedBookInformation={updatedBookInformation}
          closeCreateArea={closeCreateArea}
        />
      ) : null}
      <br />
      <br />
      <Footer />
    </div>
  );
}

export default App;
