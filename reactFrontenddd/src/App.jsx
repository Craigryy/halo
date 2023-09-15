import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import CategoryList from './components/categoryList';
import CreateArea from './components/CreateArea';
import Header from './components/Header';
import Footer from './components/Footer';
import { useNavigate } from 'react-router-dom';
import { useCookies } from 'react-cookie';
import './App.css';
import Login from './components/login';
import User from './components/User';
import APIService from './APIService'; 

function App() {
  const [categories, setCategories] = useState([]);
  const [token, setToken, removeCookie] = useCookies(['mytoken']);
  const navigate = useNavigate();
  const [books, setBooks] = useState([]);
  const [users, setUsers] = useState([]);
  const [editedCategory, setEditedCategory] = useState(null);
  const [editedBook, setEditedBook] = useState(null);
  const [showBooks, setShowBooks] = useState({});
  const [editedCategories, setEditedCategories] = useState(null);

  useEffect(() => {
    // Use APIService to fetch categories
    APIService.makeRequest('/categories/', 'GET', null, token['mytoken'])
      .then(resp => setCategories(resp))
      .catch(error => console.log(error));
  }, [token]);
  
  useEffect(() => {
    // Use APIService to fetch books
    APIService.makeRequest('/books/', 'GET', null, token['mytoken'])
      .then(resp => setBooks(resp))
      .catch(error => console.log(error));
  }, [token]);
 
   
  useEffect(() => {
    if (!token['mytoken']) {
      navigate('/'); // Use navigate() to redirect to the '/' route
    }
  }, [token, navigate]);

  const editCat = (category) => {
    setEditedCategories(category);
  };

  const editCatBook = (book) => {
    setEditedBook(book);
  };

  const fetchCategories = () => {
    APIService.makeRequest('/categories/', 'GET', null, token['mytoken'])
    .then(resp => setCategories(resp))
    .catch(error => console.log(error));
    };  


  const fetchBooks = () => {
    APIService.makeRequest('/books/', 'GET', null, token['mytoken'])
    .then(resp => setBooks(resp))
    .catch(error => console.log(error));
    };  
   

  const fetchUsers = () => {
    APIService.makeRequest('/users/', 'GET', null, token['mytoken'])
    .then(resp => setUsers(resp))
    .catch(error => console.log(error));
    };  

  const updatedInformation = (category) => {
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

  const updatedBookInformation = (book) => {
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

  const insertedInformation = (category) => {
    const new_categories = [...categories, category];
    setCategories(new_categories);
    setEditedCategories(null);
    fetchCategories();
    fetchBooks();
  };

  const deleteBtn = (category) => {
    const new_category = categories.filter(mycategory => mycategory.id !== category.id);
    setCategories(new_category);
    fetchCategories();
    fetchBooks();
  };

  const logoutBtn = () => {
    removeCookie('mytoken');
    navigate('/');
  };

  const deleteBtnBook = (book) => {
    const new_Books = books.filter(myBooks => myBooks.id !== book.id);
    setBooks(new_Books);
    fetchBooks();
    fetchCategories();
  };

  const handleEditCategory = (category) => {
    setEditedCategory(category);
  };

  const handleEditBook = (book) => {
    setEditedBook(book);
  };

  const toggleShowBooks = (categoryId) => {
    setShowBooks((prevShowBooks) => ({
      ...prevShowBooks,
      [categoryId]: !prevShowBooks[categoryId],
    }));
  };

  const openCreateArea = () => {
    setEditedCategory({ name: '', created_by: '' });
  };

  const insertedBookInformation = (book) => {
    const new_books = [...books, book];
    setBooks(new_books);
    setEditedBook(null);
    fetchCategories();
    fetchBooks();
  };

  const navigateToUserRoute = () => {
    navigate('/user');
  };

  const deleteBtnUser = (user) => {
    const new_user = users.filter(myuser => myuser.id !== user.id);
    setUsers(new_user);
    fetchUsers();
    fetchCategories();
  };
  return (
    <div className="App">
      <div className="row">
        <div className="col">
          <Header title="Halo" />
        </div>
        <div className="col text-right"> {/* Use Bootstrap's text-right class */}
          <button onClick={logoutBtn} className='btn btn-primary custom-btn'>
            Logout
          </button>
        </div>
      </div>
      <br />
      <br />
      <button className="btn btn-success custom-btn" onClick={openCreateArea}>
        INSERT
      </button>
      {editedCategory || editedBook ? (
        <CreateArea
          category={editedCategory}
          book={editedBook}
          updatedInformation={updatedInformation}
          insertedInformation={insertedInformation}
          insertedBookInformation={insertedBookInformation}
          updatedBookInformation={updatedBookInformation}
        />
      ) : null }
      <CategoryList
        categories={categories}
        books={books}
        users={users}
        showBooks={showBooks}
        toggleShowBooks={toggleShowBooks}
        editCat={handleEditCategory}
        editCatBook={handleEditBook}
        deleteBtn={deleteBtn}
        deleteBtnBook={deleteBtnBook}
        fetchUsers={fetchUsers}
      />
      <User deleteBtnUser={deleteBtnUser} />
      <Footer />
    </div>
  );
}

export default App;