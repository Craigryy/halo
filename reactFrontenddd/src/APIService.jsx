export default class APIService {
  static async makeRequest(url, method, body = null, token = null) {
    const headers = {
      "Content-Type": "application/json",
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
    const requestOptions = {
      method,
      headers,
    };

    if (body) {
      requestOptions.body = JSON.stringify(body);
    }

    const response = await fetch(url, requestOptions);
    const data = await response.json();
    return data;
  }

  // get all categories from the server and store them in state

  static async insertCategory(body, token) {
    return fetch(`/categories/add`, {
      method: "POST",
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })
    .then(resp => {
      if (!resp.ok) {
        throw new Error(`Error: ${resp.status} ${resp.statusText}`);
      }
      return resp.json();
    })
    .catch(error => {
      console.error('Error inserting category:', error);
    });
  }

  static async UpdateCategory (categoryId, updatedData, token) {
    return fetch(`/categories/${categoryId}/`, {
        method: 'PUT', 
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(updatedData)
      })
      .then(resp => {
        if (!resp.ok) {
          throw new Error(`Error: ${resp.status} ${resp.statusText}`);
        }
        return resp.json();
      })
      .catch(error => {
        console.error('Error inserting category:', error);
      });
    }

   static async DeleteCategory (categoryId, token)  {
    return fetch(`/categories/${categoryId}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to delete category');
      }
    })
    .catch(error => {
      throw error;
    });
}


  
  //  BOOKS ROUTES

  static async addBook(id,body, token) {
    return fetch(`/categories/${id}/books/`, {
      method: "POST",
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })
    .then(resp => {
      if (!resp.ok) {
        throw new Error(`Error: ${resp.status} ${resp.statusText}`);
      }
      return resp.json();
    })
    .catch(error => {
      console.error('Error adding book:', error);
      console.error('Response body:', error.response);
    });
  }

  static async getAllBooks(token) {
    return fetch('/books/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    .then(resp => {
      if (!resp.ok) {
        throw new Error(`Error: ${resp.status} ${resp.statusText}`);
      }
      return resp.json();
    })
    .catch(error => {
      console.error('Error fetching all books:', error);
    });
  }
  

  static async updateBook (categoryId, bookId,updatedData, token) {
    return fetch(`/categories/${categoryId}/books/${bookId}`, {
        method: 'PUT', 
        headers: {
          'Content-Type': 'application/json',
         'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(updatedData)
      })
      .then(resp => {
        if (!resp.ok) {
          throw new Error(`Error: ${resp.status} ${resp.statusText}`);
        }
        return resp.json();
      })
      .catch(error => {
        console.error('Error inserting book:', error);
      });
    }



  static async deleteBook (categoryId,bookId, token)  {
    return fetch(`/categories/${categoryId}/books/${bookId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to delete book');
      }
    })
    .catch(error => {
      throw error;
    });
  }   
  
  //  Login Routes

static async login(username, password) {
  const url = '/login';
  const body = { name: username, password };

  return fetch(url, {
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Login failed. Please check your credentials and try again.');
    }
    return response.json();
  })
  .then(data => {
    const token = data.access_token;
    return token;
  })
  .catch(error => {
    console.error('Error fetching token:', error);
    throw new Error('Login failed. Please check your credentials and try again.');
  });
}

  // / Users Routes

  static async createUser(username, password) {
    const requestBody = {
      name: username,
      password: password
    };
  
    return fetch('/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`Error: ${response.status} ${response.statusText}`);
        }
        return response.json();
      })
      .catch(error => {
        console.error('Error creating user:', error);
      });
  }
  

  static async getAllUsers(token) {
    return fetch("/users", {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    .then(resp => {
      if (!resp.ok) {
        throw new Error(`Error: ${resp.status} ${resp.statusText}`);
      }
      return resp.json();
    })
    .catch(error => {
      console.error('Error fetching all users:', error);
    });
  }
  static async deleteUser (Id, token)  {
    return fetch(`/user/${Id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to delete a user');
      }
    })
    .catch(error => {
      throw error;
    });
  } 
  


}





