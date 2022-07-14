import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

function CreateDeployment(props) {
    const [projectId] = useState(props.projectId);
    const [modelId] = useState(props.modelId);
    const [models, setModels] = useState(null);
    const selectModelsRef = useRef(null);

    useEffect(() => {
        axios.get('/models', {
            params: {
                project_id: parseInt(projectId)
            },
            headers: {
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            let models = [];
            for (let i = 0; i < response.data.length; i++) {
                if (response.data[i].id !== parseInt(modelId) && response.data[i].is_trained) {
                    models.push(response.data[i]);
                }
            }
            setModels(models);
            setTimeout(() => {
                window.selectSecondaryModels = window.$(selectModelsRef.current).selectize({
                    maxItems: 1
                });
            }, 100);
        }).catch((error) => {
        });
    }, []);

    const deploymentCreation = function () {
        document.getElementById('error-div').classList.add('d-none');
        document.getElementById('next-btn').classList.add('disabled');
        window.$("#loading-btn").html('<div class="spinner-border spinner-border-sm text-white me-1" role="status"></div>');

        if (document.getElementById("deployment-name").value === '') {
            document.getElementById('error-msg').innerHTML = 'Deployment name is required.';
            document.getElementById('error-div').classList.remove('d-none');
            document.getElementById('next-btn').classList.remove('disabled');
            window.$("#loading-btn").html('<i className="fe-check-circle me-1"></i>');
            return;
        }

        let selectedModel = window.selectSecondaryModels[0].selectize.getValue();
        let deploymentType = window.$("input[name=deploymenttype]:checked").val();

        if (selectedModel !== '' && deploymentType === 'single_model') {
            document.getElementById('error-msg').innerHTML = 'Single Model selected with a model. Please select Champion-Challenger type.';
            document.getElementById('error-div').classList.remove('d-none');
            document.getElementById('next-btn').classList.remove('disabled');
            window.$("#loading-btn").html('<i className="fe-check-circle me-1"></i>');
            return;
        }

        if (selectedModel === '' && deploymentType !== 'single_model') {
            document.getElementById('error-msg').innerHTML = 'Champion-Challenger and Secondary Model not selected.';
            document.getElementById('error-div').classList.remove('d-none');
            document.getElementById('next-btn').classList.remove('disabled');
            window.$("#loading-btn").html('<i className="fe-check-circle me-1"></i>');
            return;
        }

        let data = {
            project_id: parseInt(projectId),
            name: document.getElementById("deployment-name").value,
            primary_model_id: parseInt(modelId),
            secondary_model_id: parseInt(selectedModel),
            type: deploymentType,
            is_running: window.$("input[name=deployment-action]:checked").val()
        };

        axios.post(`/deployments`, data, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            window.location.href = `/${projectId}/deployments`;
        }).catch((error) => {
            document.getElementById('next-btn').classList.remove('disabled');
            window.$("#loading-btn").html('<i className="fe-check-circle me-1"></i>');
        });

    }

    return (
        <div className="row">
            <div className="col-12">
                <div className="card">
                    <div className="card-body">
                        <div className="row">
                            <div className="col-xl-6">
                                {/* DEPLOYMENT NAME */}
                                <div className="mb-3">
                                    <label htmlFor="deployment-name" className="form-label">Deployment Name:</label>
                                    <input type="text" id="deployment-name" className="form-control" placeholder="Enter deployment name" />
                                </div>
                                {/* CHAMPION-CHALLENGER / CHAMPION */}
                                <div className="mb-3">
                                    <label className="form-label">Deployment Type:</label><br />
                                    <div className="form-check form-check-inline">
                                        <input type="radio" id="customRadio1" name="deploymenttype" className="form-check-input" value='champion_challenger' />
                                        <label className="form-check-label" htmlFor="customRadio1">Champion-Challenger</label>
                                    </div>
                                    <div className="form-check form-check-inline">
                                        <input type="radio" id="customRadio2" name="deploymenttype" className="form-check-input" value='single_model' defaultChecked />
                                        <label className="form-check-label" htmlFor="customRadio2">Single Model</label>
                                    </div>
                                </div>
                                <div className="mb-2">
                                    <div id='error-div' className="mt-4 d-none">
                                        <label id="error-msg" className="text-danger"></label>
                                    </div>
                                </div>
                            </div>
                            <div className="col-xl-6">
                                <div className="mb-3">
                                    <label htmlFor="models-select" className="form-label">Select Secondary Model:</label>
                                    <select id="models-select" ref={selectModelsRef}>
                                        {models !== null ?
                                            models.map((model, index) => {
                                                return (
                                                    <option key={index} value={model.id}>{model.name}</option>
                                                );
                                            })
                                            : null}
                                    </select>
                                </div>
                                {/* ENABLE/DISABLE DEPLOYMENT */}
                                <div className="mb-3">
                                    <label className="form-label">Run Deployment (After Creation):</label><br />
                                    <div className="form-check form-check-inline">
                                        <input type="radio" id="customRadio1" name="deployment-action" className="form-check-input" defaultChecked />
                                        <label className="form-check-label" htmlFor="customRadio1">Enable</label>
                                    </div>
                                    <div className="form-check form-check-inline">
                                        <input type="radio" id="customRadio2" name="deployment-action" className="form-check-input" />
                                        <label className="form-check-label" htmlFor="customRadio2">Disable</label>
                                    </div>
                                </div>
                                {/* CREATE / CANCEL */}
                                <div className="row float-end">
                                    <div className="col-12 text-center">
                                        <a href={`/${projectId}/deployments`} className="btn btn-light waves-effect waves-light m-1"><i className="fe-x me-1"></i>Cancel</a>
                                        <button id="next-btn" type="button" className="btn btn-success waves-effect waves-light m-1" onClick={deploymentCreation}>
                                            <div id="loading-btn" className="d-inline">
                                                <i className="fe-check-circle me-1"></i>
                                            </div>
                                            Create
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default CreateDeployment;