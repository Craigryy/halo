import React, { useState } from 'react';
import APIService from '../APIService';
import { useCookies } from 'react-cookie';
import '../CSS/CategoryList.css';
import { Modal } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import bookicon from '../images/bookicon.png';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPencilAlt, faTrash } from '@fortawesome/free-solid-svg-icons';

/**
 * Component to display a list of categories and their respective books.
 *
 * @component
 * @param {Object} props - The properties passed to the component.
 * @param {Array} props.categories - An array of category objects.
 * @param {Array} props.books - An array of book objects.
 * @param {Object} props.showBooks - Object to manage book visibility for each category.
 * @param {Function} props.toggleShowBooks - Function to toggle book visibility.
 * @param {Function} props.editCat - Function to edit a category.
 * @param {Function} props.editCatBook - Function to edit a book.
 * @param {Function} props.deleteBtn - Function to delete a category.
 * @param {Function} props.deleteBtnBook - Function to delete a book.
 * @returns {JSX.Element} The rendered JSX element.
 */
function CategoryList(props) {
  const { categories, books } = props;
  const [allBooks, setAllBooks] = useState([]);
  const [showAllBooks, setShowAllBooks] = useState(false);
  const [token] = useCookies(['mytoken']);
  const [showModal, setShowModal] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(null);

/**
 * Fetches all books and updates the component state with the fetched books.
 *
 * @function
 * @returns {void}
 */
const fetchAllBooks = () => {
  APIService.getAllBooks(token['mytoken'])
    .then(response => {
      setAllBooks(response);
    })
    .catch(error => {
      console.error('Error fetching all books:', error);
    });
};


  /**
 * Toggles the display of all books.
 *
 * @function
 * @returns {void}
 */
const toggleShowAllBooks = () => {
  setShowAllBooks(prevShowAllBooks => !prevShowAllBooks);
  if (!showAllBooks) {
    fetchAllBooks();
  }
};


  /**
   * Edits a category.
   *
   * @function
   * @param {Object} category - The category to edit.
   */
  const editCat = category => {
    props.editCat(category);
  };

  /**
   * Edits a book within a category.
   *
   * @function
   * @param {Object} book - The book to edit.
   */
  const editCatBook = book => {
    props.editCatBook(book);
  };

  /**
   * Deletes a category.
   *
   * @function
   * @param {Object} category - The category to delete.
   */
  const deleteCategory = category => {
    const isConfirmed = window.confirm('Are you sure you want to delete this category?');
    if (isConfirmed) {
      APIService.DeleteCategory(category.id, token['mytoken'])
        .then(() => props.deleteBtn(category))
        .catch(error => {
          console.error('Error deleting category:', error);
        });
    }
  };

  /**
   * Deletes a book.
   *
   * @function
   * @param {Object} book - The book to delete.
   */
  const deleteBook = book => {
    const isConfirmed = window.confirm('Are you sure you want to delete this book?');
    if (isConfirmed) {
      APIService.deleteBook(book.category_id, book.id, token['mytoken'])
        .then(() => props.deleteBtnBook(book))
        .catch(error => {
          console.error('Error deleting book:', error);
        });
    }
  };

  /**
   * Handles showing the modal with books for a category.
   *
   * @function
   * @param {Object} category - The selected category.
   */
  const handleShowModal = category => {
    setSelectedCategory(category);
    setShowModal(true);
  };

  /**
   * Handles closing the modal.
   *
   * @function
   */
  const handleCloseModal = () => {
    setShowModal(false);
  };

  return (
    <div className="CategoryList">
      {categories && categories.length > 0 ? (
        categories.map(category => (
          <div className="key" key={category.id}>
            <h3>{category.name}</h3>
            <p>Created by: {category.created_by}</p>
            <div className="col">
              <button className="btn btn-primary" onClick={() => editCat(category)}>
                <FontAwesomeIcon icon={faPencilAlt} />
              </button>
              <button className="btn btn-danger" onClick={() => deleteCategory(category)}>
                <FontAwesomeIcon icon={faTrash} />
              </button>
            </div>
            <span onClick={() => handleShowModal(category)}>
              {props.showBooks[category.id] ? 'Hide Books' : 'show books'}{' '}
            </span>
          </div>
        ))
      ) : (
        <div className="no-categories">
          <div className="grey-background">
            <img
              src={bookicon}
              alt="Book Icon"
              style={{ width: '48px', height: '48px', color: 'blue' }}
            />
          </div>
          <p>You do not have any book to read at the moment.</p>
        </div>
      )}

      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title></Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {books
            .filter(book => selectedCategory && book.category_id === selectedCategory.id)
            .map(book => (
              <div key={book.id} className="book">
                <h3>{book.title}</h3>
                <p>Author: {book.author}</p>
                <div className="book-actions">
                  <button className="btn btn-primary custom-btn" onClick={() => editCatBook(book)}>
                    <FontAwesomeIcon icon={faPencilAlt} />
                  </button>
                  <button className="btn btn-danger custom-btn" onClick={() => deleteBook(book)}>
                    <FontAwesomeIcon icon={faTrash} />
                  </button>
                </div>
              </div>
            ))}
          {books.filter(book => selectedCategory && book.category_id === selectedCategory.id)
            .length === 0 && <div>No books available</div>}
        </Modal.Body>
        <Modal.Footer>
          <button className="btn btn-secondary" onClick={handleCloseModal}>
            Close
          </button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default CategoryList;
