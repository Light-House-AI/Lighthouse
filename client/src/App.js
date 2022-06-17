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
import CreateModelPage from './pages/CreateModelPage';
import CreateDeploymentPage from './pages/CreateDeploymentPage';
import ViewDatasetPage from './pages/ViewDatasetPage';
import CleanDataPage from './pages/CleanDataPage';
import RulesDataPage from './pages/RulesDataPage';
function App() {

  useEffect(() => {
    axios.defaults.baseURL = "http://localhost:8000/api/v1";
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/newproject" element={<CreateProjectPage />} />
        <Route path="/:projectid" element={<DatasetsPage />} />
        <Route path="/:projectid/datasets" element={<DatasetsPage />} />
        <Route path="/:projectid/models" element={<ModelsPage />} />
        <Route path="/:projectid/deployments" element={<DeploymentsPage />} />
        <Route path="/:projectid/models/create" element={<CreateModelPage />} />
        <Route path="/:projectid/models/:datasetcleanedid/create" element={<CreateModelPage />} />
        <Route path="/:projectid/deployments/create" element={<CreateDeploymentPage />} />
        <Route path="/:projectid/datasets/:datasettype/:datasetid/view" element={<ViewDatasetPage />} />
        <Route path="/:projectid/datasets/:datasetsid/clean" element={<CleanDataPage />} />
        <Route path="/:projectid/datasets/:datasetid/rules" element={<RulesDataPage />} />
        <Route path="/sample" element={<Sample />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
