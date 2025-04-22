export default class APIService {
  static API_URL = process.env.REACT_APP_API_URL || '';

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

    const fullUrl = `${this.API_URL}${url}`;
    const response = await fetch(fullUrl, requestOptions);
    const data = await response.json();
    return data;
  }

  // get all categories from the server and store them in state

  static async insertCategory(body, token) {
    return this.makeRequest(`/categories/add`, 'POST', body, token);
  }

  static async UpdateCategory(categoryId, updatedData, token) {
    return this.makeRequest(`/categories/${categoryId}/`, 'PUT', updatedData, token);
  }

  static async DeleteCategory(categoryId, token) {
    return this.makeRequest(`/categories/${categoryId}/`, 'DELETE', null, token);
  }

  //  BOOKS ROUTES

  static async addBook(categoryId, body, token) {
    return this.makeRequest(`/categories/${categoryId}/books/`, 'POST', body, token);
  }

  static async getAllBooks(token) {
    return this.makeRequest('/books/', 'GET', null, token);
  }

  static async updateBook(categoryId, bookId, updatedData, token) {
    return this.makeRequest(`/categories/${categoryId}/books/${bookId}`, 'PUT', updatedData, token);
  }

  static async deleteBook(categoryId, bookId, token) {
    return this.makeRequest(`/categories/${categoryId}/books/${bookId}`, 'DELETE', null, token);
  }


  //  Login Routes

static async login(username, password) {
  const url = '/login';
  const body = { name: username, password };

  return fetch(`${this.API_URL}${url}`, {
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

    return this.makeRequest('/auth/register', 'POST', requestBody);
  }

  static async getAllUsers(token) {
    return this.makeRequest('/users', 'GET', null, token);
  }

  static async deleteUser(id, token) {
    return this.makeRequest(`/user/${id}/`, 'DELETE', null, token);
  }
}
