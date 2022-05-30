import React, { useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import "bootstrap";
import './scss/icons.scss';
import './scss/structure.scss';

import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import Sample from './pages/Sample'
import DatasetsPage from './pages/DatasetsPage';
import ModelsPage from './pages/ModelsPage';
import DeploymentsPage from './pages/DeploymentsPage';
import CreateProjectPage from './pages/CreateProjectPage';
import ViewDatasetPage from './pages/ViewDatasetPage';

function App() {

  useEffect(() => {
    axios.defaults.baseURL = "http://localhost:3000/api";
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<HomePage />} />
        <Route path="/newproject" element={<CreateProjectPage />} />
        <Route path="/:projectid" element={<DatasetsPage />} />
        <Route path="/:projectid/datasets" element={<DatasetsPage />} />
        <Route path="/:projectid/models" element={<ModelsPage />} />
        <Route path="/:projectid/deployments" element={<DeploymentsPage />} />
        <Route path="/:projectid/datasets/:datasetid/view" element={<ViewDatasetPage />} />
        <Route path="/sample" element={<Sample />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
