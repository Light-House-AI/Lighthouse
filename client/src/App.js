import React from 'react';
import axios from 'axios';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import "bootstrap";
import './scss/icons.scss';
import './scss/structure.scss';
import Homepage from './pages/Homepage';

function App() {
  axios.defaults.baseURL = "http://localhost:3000/api";

  return (
    <div id='wrapper'>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Homepage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
