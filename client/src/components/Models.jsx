import React, { useState, useEffect, useRef } from "react";
import ReactDOM from 'react-dom/client';
import axios from "axios";

import GenericModal from './structure/GenericModal';

function Models(props) {
    const tableRef = useRef(null);
    const [projectId] = useState(props.projectId);
    const [type] = useState(props.type);
    const [models, setModels] = useState(null);
    const [cleanedDatasets, setCleanedDatasets] = useState(null);
    const [rootCreated, setRootCreated] = useState(false);
    const [reactRoot, setReactRoot] = useState(null);

    useEffect(() => {
        window.tippy('[data-plugin="tippy"]', {
            placement: 'left',
            followCursor: 'false',
            arrow: 'true'
        });

        axios.get(`/datasets/cleaned`, {
            params: {
                project_id: projectId
            },
            headers: {
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setCleanedDatasets(response.data);
            axios.get('/models', {
                params: {
                    project_id: projectId
                },
                headers: {
                    'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
                }
            }).then((response) => {
                setModels(response.data);
                setTimeout(() => {
                    window.$(tableRef.current).footable();
                }, 100)
            }).catch((error) => {
            });
        }).catch((error) => {
        });
    }, []);

    const createModel = () => {
        if (cleanedDatasets.length === 0 || cleanedDatasets === null)
            return;

        var modalBody = reactRoot;
        if (!rootCreated) {
            modalBody = ReactDOM.createRoot(window.$("#modal-structure #modal-body")[0])
            setRootCreated(true);
            setReactRoot(modalBody);
        }

        let selectDS =
            <div className="h-50 my-2">
                <label className="form-label">Select Dataset:</label><br />
                <select id="select-multiple-datasets">
                    {cleanedDatasets !== null ?
                        cleanedDatasets.map((dataset, index) => {
                            return (
                                <option key={index} value={dataset.id}>{dataset.name}</option>
                            )
                        })
                        : null}
                </select>
            </div>;
        modalBody.render(selectDS);

        window.$("#modal-structure #modal-title").text("Create new cleaned dataset");
        setTimeout(() => {
            window.selectizeModal = window.$("#modal-structure #select-multiple-datasets").selectize({
                maxItems: 1
            });
        }, 100);

        window.$("#modal-structure #modal-btn").on('click', function () {
            let datasetsId = window.selectizeModal[0].selectize.getValue();
            if (datasetsId !== '' && datasetsId !== null && datasetsId !== [] && datasetsId !== undefined) {
                window.location.href = `/${projectId}/models/${datasetsId}/create`;
            }
        });

        document.getElementById('modal-trigger').click();
    }

    const findDatasetName = function (dataset_id) {
        for (let i = 0; i < cleanedDatasets.length; i++) {
            if (cleanedDatasets[i].id === dataset_id) {
                return cleanedDatasets[i].name;
            }
        }
    }

    return (
        <div className="row">
            <div className="col-12">
                <div className="row">
                    <div className="col-6">
                        <h4 className="header-title mb-0 h-100 d-flex align-items-center">All Models</h4>
                    </div>
                    <div className="col-6">
                        <button className="button-no-style float-end" title="Create new model" data-plugin="tippy" onClick={createModel}>
                            <i className="fe-plus noti-icon text-color btn-link"></i>
                        </button>
                    </div>
                </div>
                <div className="table-responsive pt-3">
                    <table ref={tableRef} className="table table-centered table-nowrap table-borderless mb-0" data-sort="false">
                        <thead className="table-light">
                            <tr>
                                <th data-toggle="true">Name</th>
                                <th>Created At</th>
                                <th>Status</th>
                                <th>Metric(Accuracy/MSLE)</th>
                                <th data-hide="all">Dataset names</th>
                                <th data-hide="all">Number of Layers</th>
                                <th data-hide="all">Maximum Neurons/Layer</th>
                                <th data-hide="all">Learning Rate</th>
                                <th data-hide="all">Batch Size</th>
                            </tr>
                        </thead>
                        <tbody>
                            {models !== null ?
                                models.map((model, index) => {
                                    return (
                                        <tr key={index}>
                                            <td>{model.name}</td>
                                            <td>{(new Date(model.created_at).toLocaleString('en-CA', { month: 'short', day: 'numeric', year: 'numeric' }))}</td>
                                            {model.is_trained ?
                                                <td><span className="badge bg-soft-success text-success p-1">Completed</span></td> :
                                                <td><span className="badge bg-soft-warning text-warning p-1">In progress</span></td>
                                            }
                                            {type === 'classification' && model.is_trained ?
                                                <td>{model.score !== null ? model.score * 100 : ''}%</td> :
                                                null
                                            }
                                            {type !== 'classification' && model.is_trained ?
                                                <td>{model.score}</td> :
                                                null
                                            }
                                            {!model.is_trained ?
                                                <td>-</td> : null
                                            }
                                            <td>{findDatasetName(model.dataset_id)}</td>
                                            <td>{model.number_of_layers}</td>
                                            <td>{model.maximum_neurons_per_layer}</td>
                                            <td>{model.learning_rate}</td>
                                            <td>{model.batch_size}</td>
                                        </tr>
                                    );
                                }) : null}
                        </tbody>
                    </table>
                </div>
                <GenericModal hideNext={false} />
            </div>
        </div>
    );
}

export default Models;