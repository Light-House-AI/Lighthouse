import React, { useState, useEffect } from "react";
import ReactDOM from 'react-dom/client';
import axios from "axios";

import GenericModal from './structure/GenericModal';

function Deployments(props) {
    const [projectId] = useState(props.projectId);
    const [rootCreated, setRootCreated] = useState(false);
    const [reactRoot, setReactRoot] = useState(null);
    const [deployments, setDeployments] = useState(null);
    const [models, setModels] = useState(null);

    useEffect(() => {
        window.tippy('[data-plugin="tippy"]', {
            placement: 'left',
            followCursor: 'false',
            arrow: 'true'
        });

        axios.get('/models', {
            params: {
                project_id: parseInt(projectId)
            },
            headers: {
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setModels(response.data);
        }).catch((error) => {
        });

        axios.get('/deployments', {
            params: {
                project_id: projectId
            },
            headers: {
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setDeployments(response.data);
        }).catch((error) => {
        });

        window.$("#testing").footable();
    }, []);

    const createDeployment = () => {
        if (deployments.length === 0 || deployments === null)
            return;

        var modalBody = reactRoot;
        if (!rootCreated) {
            modalBody = ReactDOM.createRoot(window.$("#modal-structure #modal-body")[0])
            setRootCreated(true);
            setReactRoot(modalBody);
        }

        let selectDS =
            <div className="h-50 my-2">
                <label className="form-label">Select Model:</label><br />
                <select id="select-multiple-model">
                    {deployments !== null ?
                        deployments.map((dataset, index) => {
                            return (
                                <option key={index} value={dataset.id}>{dataset.name}</option>
                            )
                        })
                        : null}
                </select>
            </div>;
        modalBody.render(selectDS);

        window.$("#modal-structure #modal-title").text("Create new deployment");
        setTimeout(() => {
            window.selectizeModal = window.$("#modal-structure #select-multiple-model").selectize({
                maxItems: 1
            });
        }, 100);

        window.$("#modal-structure #modal-btn").on('click', function () {
            let modelId = window.selectizeModal[0].selectize.getValue();
            if (modelId !== '' && modelId !== null && modelId !== [] && modelId !== undefined) {
                window.location.href = `/${projectId}/deployments/${modelId}/create`;
            }
        });

        document.getElementById('modal-trigger').click();
    }

    const findModelName = function () {
        for (let i = 0; i < models.length; i++) {
            if (models[i].id === this.dataset_id) {
                return models[i].name;
            }
        }
    }

    return (
        <div className="row">
            <div className="col-12">
                <div className="row">
                    <div className="col-6">
                        <h4 className="header-title mb-0 h-100 d-flex align-items-center">All Deployments</h4>
                    </div>
                    <div className="col-6">
                        <button className="button-no-style float-end" title="Add new deployment" data-plugin="tippy" onClick={createDeployment}>
                            <i className="fe-plus noti-icon text-color btn-link"></i>
                        </button>
                    </div>
                </div>
                <div className="table-responsive pt-3">
                    <table id="testing" className="table table-centered table-nowrap table-borderless mb-0" data-sort="false">
                        <thead className="table-light">
                            <tr>
                                <th data-toggle="true">Name</th>
                                <th>Created At</th>
                                <th>Type</th>
                                <th>Status</th>
                                <th>Monitoring</th>
                                <th>Action</th>
                                <th data-hide="all">Primary Model</th>
                                <th data-hide="all">Secondary Model</th>
                            </tr>
                        </thead>
                        <tbody>
                            {deployments !== null ?
                                deployments.map((deployment, index) => {
                                    return (
                                        <tr key={index}>
                                            <td>{deployment.name}</td>
                                            <td>{(new Date(deployment.created_at).toLocaleString('en-CA', { month: 'short', day: 'numeric', year: 'numeric' }))}</td>
                                            {deployment.type === 'champion_challenger' ?
                                                <td><span className="badge bg-soft-info text-info p-1">Champion - Challenger</span></td> :
                                                <td><span className="badge bg-soft-warning text-warning p-1">Fallout</span></td>
                                            }
                                            {deployment.is_running ?
                                                <td><span className="badge bg-soft-success text-success p-1">Active</span></td> :
                                                <td><span className="badge bg-soft-danger text-danger p-1">Disabled</span></td>
                                            }
                                            {deployment.is_running ?
                                                <td><button className="btn btn-outline-success btn-sm rounded-pill">View</button></td> :
                                                <td><button className="btn btn-outline-success btn-sm rounded-pill disabled">View</button></td>
                                            }
                                            {deployment.is_running ?
                                                <td><button className="btn btn-outline-danger btn-sm rounded-pill">Disable</button></td> :
                                                <td><button className="btn btn-outline-success btn-sm rounded-pill">Enable</button></td>
                                            }
                                            <td>{findModelName(deployment.primary_model_id)}</td>
                                            <td>{deployment.type === 'champion_challenger' ? deployment.secondary_model_id : 'No secondary model'}</td>
                                        </tr>
                                    )
                                })
                                : null}
                        </tbody>
                    </table>
                </div>
                <GenericModal hideNext={false} />
            </div>
        </div>
    );
}

export default Deployments;