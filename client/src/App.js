import { BrowserRouter, Route, Routes } from 'react-router-dom';
import axios from 'axios';

import Homepage from './pages/Homepage';

function App() {
  axios.defaults.baseURL = "http://localhost:3000/api";
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Homepage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
