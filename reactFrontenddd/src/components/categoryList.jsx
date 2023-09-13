import React, { useState } from 'react';
import APIService from '../APIService';
import { useCookies } from 'react-cookie';

function CategoryList(props) {
  // Destructuring props
  const { categories, books, users } = props;

  // State variables
  const [token, setToken, removeCookie] = useCookies(['mytoken']);
  const [allBooks, setAllBooks] = useState([]);
  const [allUsers, setAllUsers] = useState([]);
  const [showAllBooks, setShowAllBooks] = useState(false);
  const [showAllUsers, setShowAllUsers] = useState(false);


  const toggleShowAllUsers = () => {
      // a toggle to show books
    setShowAllUsers(prevShowAllUsers => !prevShowAllUsers);
  };


  const fetchAllBooks = () => {
    // call the getAllBooks from APIService,taking in the token 
    APIService.getAllBooks(token['mytoken'])
      .then(response => {
        setAllBooks(response);
      })
      .catch(error => {
        console.error('Error fetching all books:', error);
      });
  };

  const editCat = (category) => {
    // create a function  called editCategory,take in a category as an input and send props to App.js
    props.editCat(category);
  };

  const editCatBook = (book) => {
    // create a function  called editCategoryBook,take in a book as an input and send props to App.js
    props.editCatBook(book);
  };

  const deleteCategory = (category) => {
    const isConfirmed = window.confirm("Are you sure you want to delete this category?");

    if (isConfirmed) {
    // calls the DeleteCategory from APIService,taking in category id and token 
      APIService.DeleteCategory(category.id, token['mytoken'])
      // pass in the props to App.js
        .then(() => props.deleteBtn(category))
        .catch((error) => {
          console.error('Error deleting category:', error);
        });
    }
  };

  const deleteBook = (book) => {
    const isConfirmed = window.confirm("Are you sure you want to delete this book?");

    if (isConfirmed) {
    // calls the deleteBook from APIService,taking in categoryID, bookID and token 
      APIService.deleteBook(book.category_id, book.id, token['mytoken'])
      // pass in the props to App.js
        .then(() => props.deleteBtnBook(book))
        .catch((error) => {
          console.error('Error deleting book:', error);
        });
    }
  };

  return (
    <div>
      {/* check if there are categories, if there is iterate over them */}
      {categories && categories.length > 0 ? (
        categories.map((category) => (
          <div key={category.id}>
            <h3>{category.name}</h3>
            <p>created_by: {category.created_by}</p>
            <p>category_id: {category.id}</p>
            <br/>

            <div className="row">
              <div className="col-md-1">
                <button className="btn btn-primary" onClick={() => editCat(category)}>
                  Update
                </button>
              </div>
              <div className="col">
                <button className="btn btn-danger" onClick={() => deleteCategory(category)}>
                  Delete
                </button>
              </div>
            </div>
            <br/>
            <button className="btn btn-primary" onClick={() => props.toggleShowBooks(category.id)}>
              {props.showBooks[category.id] ? 'Hide Books' : 'Show Books'}
            </button>
            <br />
            <hr/>

            <div className='note'>
              {/* check if there are books, if there is iterate over them */}
              {props.showBooks[category.id] && books && books.length > 0 ? (
                books
                  .filter(book => book.category_id === category.id)
                  .map((book) => (
                    <div key={book.id}>
                      <h3>{book.title}</h3>
                      <p>Author: {book.author}</p>
                      <p>Category: {book.category_id}</p>
                      <button className='btn btn-primary custom-btn' onClick={() => editCatBook(book)}>
                        Upd
                      </button>
                      <button className='btn btn-danger custom-btn' onClick={() => deleteBook(book)}>
                        Del
                      </button>
                    </div>
                  ))
              ) : null}
            </div>
          </div>
        ))
      ) : (
        <p>No categories available.</p>
      )}
    </div>
  );
}

export default CategoryList;