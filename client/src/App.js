import React, { useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import "bootstrap";
import './scss/icons.scss';
import './scss/structure.scss';

import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import DatasetsPage from './pages/DatasetsPage';
import ModelsPage from './pages/ModelsPage';
import DeploymentsPage from './pages/DeploymentsPage';
import CreateProjectPage from './pages/CreateProjectPage';
import CreateModelPage from './pages/CreateModelPage';
import CreateDeploymentPage from './pages/CreateDeploymentPage';
import ViewDatasetPage from './pages/ViewDatasetPage';
import CleanDataPage from './pages/CleanDataPage';
import RulesDataPage from './pages/RulesDataPage';
import ViewModelPage from './pages/ViewModelPage';
import ViewDeploymentPage from './pages/ViewDeploymentPage';
import PredictPage from './pages/PredictPage';

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
        {/* DATASET */}
        <Route path="/:projectid" element={<DatasetsPage />} />
        <Route path="/:projectid/datasets" element={<DatasetsPage />} />
        <Route path="/:projectid/datasets/:datasettype/:datasetid/view" element={<ViewDatasetPage />} />
        <Route path="/:projectid/datasets/:datasetsid/clean" element={<CleanDataPage />} />
        <Route path="/:projectid/datasets/:datasetid/rules" element={<RulesDataPage />} />
        {/* MODEL */}
        <Route path="/:projectid/models" element={<ModelsPage />} />
        <Route path="/:projectid/models/:datasetcleanedid/create" element={<CreateModelPage />} />
        <Route path="/:projectid/models/:modelid/view" element={<ViewModelPage />} />
        {/* DEPLOYMENTS */}
        <Route path="/:projectid/deployments" element={<DeploymentsPage />} />
        <Route path="/:projectid/deployments/:modelid/create" element={<CreateDeploymentPage />} />
        <Route path="/:projectid/deployments/:deploymentid/predict" element={<PredictPage />} />
        <Route path="/:projectid/deployments/:deploymentid/view" element={<ViewDeploymentPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
