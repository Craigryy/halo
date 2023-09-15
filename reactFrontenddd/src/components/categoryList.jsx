// CategoryList.js

import React, { useState } from 'react';
import APIService from '../APIService';
import { useCookies } from 'react-cookie';
import '../CategoryList.css'; // Import the CSS file
import bookicon from '../images/bookicon.png'; // Import the book icon image
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPencilAlt, faTrash } from '@fortawesome/free-solid-svg-icons'; // Import Font Awesome icons for Edit and Delete

function CategoryList(props) {
  const { categories, books } = props;
  const [allBooks, setAllBooks] = useState([]);
  const [showAllBooks, setShowAllBooks] = useState(false);
  const [token] = useCookies(['mytoken']);

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

  const editCat = (category) => {
    props.editCat(category);
  };

  const editCatBook = (book) => {
    props.editCatBook(book);
  };

  const deleteCategory = (category) => {
    const isConfirmed = window.confirm("Are you sure you want to delete this category?");
    if (isConfirmed) {
      APIService.DeleteCategory(category.id, token['mytoken'])
        .then(() => props.deleteBtn(category))
        .catch(error => {
          console.error('Error deleting category:', error);
        });
    }
  };

  const deleteBook = (book) => {
    const isConfirmed = window.confirm("Are you sure you want to delete this book?");
    if (isConfirmed) {
      APIService.deleteBook(book.category_id, book.id, token['mytoken'])
        .then(() => props.deleteBtnBook(book))
        .catch(error => {
          console.error('Error deleting book:', error);
        });
    }
  };

  return (
    <div className="CategoryList">
      {categories && categories.length > 0 ? (
        categories.map(category => (
          <div className="key" key={category.id}>
            <h3>{category.name}</h3>
            <p>created_by: {category.created_by}</p>
            <p>category_id: {category.id}</p>
            <div className="row">
              <div className="col-md-1">
                <button className="btn btn-primary" onClick={() => editCat(category)}>
                  <FontAwesomeIcon icon={faPencilAlt} /> {/* Edit icon */}
                </button>
              </div>
              <div className="col">
                <button className="btn btn-danger" onClick={() => deleteCategory(category)}>
                  <FontAwesomeIcon icon={faTrash} /> {/* Delete icon */}
                </button>
              </div>
            </div>
            <button className="btn btn-primary" onClick={() => props.toggleShowBooks(category.id)}>
              {props.showBooks[category.id] ? 'Hide Books' : 'Show Books'}
            </button>
            {props.showBooks[category.id] && books && books.length > 0 ? (
              <div className="book-list-background">
                <h2>All Books</h2>
                <div className="book-list">
                  {books
                    .filter(book => book.category_id === category.id)
                    .map(book => (
                      <div key={book.id} className="book">
                        <h3>{book.title}</h3>
                        <p>Author: {book.author}</p>
                        <p>Category: {book.category_id}</p>
                        <button className="btn btn-primary custom-btn" onClick={() => editCatBook(book)}>
                          <FontAwesomeIcon icon={faPencilAlt} /> {/* Edit icon */}
                        </button>
                        <button className="btn btn-danger custom-btn" onClick={() => deleteBook(book)}>
                          <FontAwesomeIcon icon={faTrash} /> {/* Delete icon */}
                        </button>
                      </div>
                    ))}
                </div>
              </div>
            ) : null}
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
    </div>
  );
}

export default CategoryList;
