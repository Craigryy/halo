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

    try {
      const response = await fetch(url, requestOptions);
      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  }

  // Categories Routes

  static async insertCategory(body, token) {
    return this.makeRequest(`/categories/add`, 'POST', body, token);
  }

  static async UpdateCategory(categoryId, updatedData, token) {
    return this.makeRequest(`/categories/${categoryId}/`, 'PUT', updatedData, token);
  }

  static async DeleteCategory(categoryId, token) {
    return this.makeRequest(`/categories/${categoryId}/`, 'DELETE', null, token);
  }

  // Books Routes

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

  // Login Routes

  static async login(username, password) {
    const url = '/login';
    const body = { name: username, password };

    return this.makeRequest(url, 'POST', body);
  }

  // Users Routes

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
