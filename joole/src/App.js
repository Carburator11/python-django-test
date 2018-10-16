import React, { Component } from 'react';
import './App.css';
import { HashRouter, Route } from "react-router-dom";
import { Home, Client } from "./"

class App extends Component {



  render() {
    return (
      <div className="App">
      <h2>Hello Watt</h2>

      <HashRouter>
        <div>
          <Route exact path="/" component={Home} />
          <Route path="/client/:id" component={Client} />
        </div>
        </HashRouter>
      </div>
    );
  }
}

export default App;
