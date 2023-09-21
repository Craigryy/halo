import React, { useState } from 'react';
import APIService from '../APIService';
import { useCookies } from 'react-cookie';
import '../CSS/CategoryList.css';
import { Modal, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import bookicon from '../images/bookicon.png';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPencilAlt, faTrash, faTimes } from '@fortawesome/free-solid-svg-icons';


function CategoryList(props) {
  const { categories, books } = props;
  const [allBooks, setAllBooks] = useState([]);
  const [showAllBooks, setShowAllBooks] = useState(false);
  const [token] = useCookies(['mytoken']);
  const [showModal, setShowModal] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(null);

  const fetchAllBooks = () => {
    APIService.getAllBooks(token['mytoken'])
      .then(response => {
        setAllBooks(response);
      })
      .catch(error => {
        console.error('Error fetching all books:', error);
      });
  };

  const toggleShowAllBooks = () => {
    setShowAllBooks(prevShowAllBooks => !prevShowAllBooks);
    if (!showAllBooks) {
      fetchAllBooks();
    }
  };

  const editCat = category => {
    props.editCat(category);
  };

  const editCatBook = book => {
    props.editCatBook(book);
  };

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

  const handleShowModal = category => {
    setSelectedCategory(category);
    setShowModal(true);
  };

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
            <div className="row">
              <div className="col-md-1">
                <button className="btn btn-primary"   onClick={() => editCat(category)}>
                  <FontAwesomeIcon icon={faPencilAlt} />
                </button>
              </div>
              <div className="col">
                <button className="btn btn-danger"   onClick={() => deleteCategory(category)}>
                  <FontAwesomeIcon icon={faTrash} />
                </button>
              </div>
            </div>
            <span onClick={() => handleShowModal(category)}>
              {props.showBooks[category.id] ? 'Hide Books' : 'show books'}{' '}
              </span>
          </div>
        ))
      ) : (
        <div className="no-categories">
          <div className="grey-background">
            <img src={bookicon} alt="Book Icon" style={{ width: '48px', height: '48px', color: 'blue' }} />
          </div>
          <p>You do not have any book to read at the moment.</p>
        </div>
      )}

      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>No available book.</Modal.Title>
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
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default CategoryList;

