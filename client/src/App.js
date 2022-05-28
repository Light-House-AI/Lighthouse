import React, { useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import "bootstrap";
import './scss/icons.scss';
import './scss/structure.scss';
import Homepage from './pages/Homepage';
import Loginpage from './pages/Loginpage';
import Sample from './pages/Sample'
function App() {

  useEffect(() => {
    axios.defaults.baseURL = "http://localhost:3000/api";
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Loginpage />} />
        <Route path="/" element={<Homepage />} />
        <Route path="/sample" element={<Sample />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
