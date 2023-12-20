import React, { Component } from 'react';
import { Navigate } from 'react-router-dom'; // Update import statement

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      loggedIn: false,
    };
  }

  handleInputChange = (e) => {
    const { name, value } = e.target;
    this.setState({ [name]: value });
  };

  handleLogin = () => {
    const { username, password } = this.state;

    // Check your login logic here
    if (username === 'aivle30' && password === '1234') {
      // Set loggedIn to true if login is successful
      this.setState({ loggedIn: true });
    }

    console.log('로그인 시도:', { username, password });
  };

  render() {
    // Redirect to /home if loggedIn is true
    if (this.state.loggedIn) {
      return <Navigate to="/" />;
    }

    return (
      <div>
        <h2>Login</h2>
        <form>
          <label>
            Username:
            <input
              type="text"
              name="username"
              value={this.state.username}
              onChange={this.handleInputChange}
            />
          </label>
          <br />
          <label>
            Password:
            <input
              type="password"
              name="password"
              value={this.state.password}
              onChange={this.handleInputChange}
            />
          </label>
          <br />
          <button type="button" onClick={this.handleLogin}>
            Login
          </button>
        </form>
      </div>
    );
  }
}

export default Login;
