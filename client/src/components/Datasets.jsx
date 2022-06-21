import React, { useState, useEffect } from "react";
import ReactDOM from 'react-dom/client';
import axios from "axios";

import GenericModal from './structure/GenericModal';

function Datasets(props) {
    const [projectId] = useState(props.projectId);
    const [rawDatasets, setRawDatasets] = useState(null);
    const [cleanedDatasets, setCleanedDatasets] = useState(null);
    const [rootCreated, setRootCreated] = useState(false);
    const [reactRoot, setReactRoot] = useState(null);

    useEffect(() => {
        window.tippy('[data-plugin="tippy"]', {
            placement: 'left',
            followCursor: 'false',
            arrow: 'true'
        });

        axios.get(`/datasets/raw/`, {
            params: {
                project_id: projectId
            },
            headers: {
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setRawDatasets(response.data);
        }).catch((error) => {
        });

        axios.get(`/datasets/cleaned/`, {
            params: {
                project_id: projectId
            },
            headers: {
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setCleanedDatasets(response.data);
        }).catch((error) => {
        });

    }, []);

    const createNewCleanedDS = () => {
        var modalBody = reactRoot;
        if (!rootCreated) {
            modalBody = ReactDOM.createRoot(window.$("#modal-structure #modal-body")[0])
            setRootCreated(true);
            setReactRoot(modalBody);
        }

        let selectDS =
            <div className="h-50 my-2">
                <label className="form-label">Select Dataset(s):</label><br />
                <select id="select-multiple-datasets">
                    {rawDatasets !== null ?
                        rawDatasets.map((dataset, index) => {
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
                maxItems: rawDatasets.length
            });
        }, 100);

        window.$("#modal-structure #modal-btn").on('click', function () {
            let datasetsId = window.selectizeModal[0].selectize.getValue();
            if (datasetsId !== '' && datasetsId !== null && datasetsId !== [] && datasetsId !== undefined) {
                if (Array.isArray(datasetsId))
                    window.location.href = `/${projectId}/datasets/${datasetsId.join('-')}/clean`;
                else
                    window.location.href = `/${projectId}/datasets/${datasetsId}/clean`;
            }
        });

        document.getElementById('modal-trigger').click();
    }

    const visualizeDataset = (e) => {
        let datasetId = window.$(e.target).attr('_id');

        var modalBody = reactRoot;
        if (!rootCreated) {
            modalBody = ReactDOM.createRoot(window.$("#modal-structure #modal-body")[0])
            setRootCreated(true);
            setReactRoot(modalBody);
        }

        let selectDS =
            <div className="h-50 my-2">
                <label className="form-label">Select Visualization:</label><br />
                <select id="select-visualization-type">
                    <option value="heatmap">Heatmap</option>
                    <option value="scatter">Scatter Chart</option>
                    <option value="line">Gradient Line Chart</option>
                    <option value="boxPlot">Box Chart</option>
                </select>
                <div className="row mt-1">
                    <div id="col-name-1" className="col-12 d-none">
                        <label className="form-label">Column Name (1st):</label>
                        <input id="col-name-1-input" type="text" className="form-control" defaultValue='' />
                    </div>
                    <div id="col-name-2" className="col-12 d-none">
                        <label className="form-label">Column Name (2nd):</label>
                        <input id="col-name-2-input" type="text" className="form-control" defaultValue='' />
                    </div>
                </div>
            </div>;
        modalBody.render(selectDS);

        window.$("#modal-structure #modal-title").text("Visualization");
        setTimeout(() => {
            window.selectizeModal = window.$("#modal-structure #select-visualization-type").selectize({
                maxItems: 1,
                onChange: function (value) {
                    if (value === 'scatter') {
                        window.$("#col-name-1").removeClass('d-none');
                        window.$("#col-name-2").removeClass('d-none');
                    } else if (value === 'box') {
                        window.$("#col-name-1").removeClass('d-none');
                        window.$("#col-name-2").addClass('d-none');
                    } else if (value === 'heatmap') {
                        window.$("#col-name-1").addClass('d-none');
                        window.$("#col-name-2").addClass('d-none');
                    } else if (value === 'pie') {
                        window.$("#col-name-1").removeClass('d-none');
                        window.$("#col-name-2").removeClass('d-none');
                    }
                }
            });
        }, 100);

        window.$("#modal-structure #modal-btn").on('click', function () {
            let type = window.selectizeModal[0].selectize.getValue();
            let colName1 = window.$("#col-name-1-input").val();
            let colName2 = window.$("#col-name-2-input").val();
            localStorage.setItem('col1', colName1);
            localStorage.setItem('col2', colName2);
            window.location.href = `/${projectId}/datasets/${datasetId}/visualize/${type}`;
        });

        document.getElementById('modal-trigger').click();
    }

    return (
        <div className="row">
            <div className="col-12">
                <div className="row">
                    <div className="col-6">
                        <h4 className="header-title mb-0 h-100 d-flex align-items-center">Raw Datasets</h4>
                    </div>
                    <div className="col-6">
                        <a href={`/${projectId}/shadow`} className="button-no-style float-end" title="View/Add Shadow Data" data-plugin="tippy">
                            <i className="fe-plus noti-icon text-color btn-link"></i>
                        </a>
                    </div>
                </div>
                <div id="cardCollpase4" className="collapse pt-3 show">
                    <div className="table-responsive">
                        {rawDatasets !== null ?
                            <table className="table align-middle table-centered table-nowrap table-borderless mb-0">
                                <thead className="table-light">
                                    <tr>
                                        <th>Name</th>
                                        <th>Created At</th>
                                        <th>Dataset</th>
                                        <th>Visulization</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {rawDatasets.map((dataset, index) => {
                                        return (
                                            <tr key={index}>
                                                <td>{window.capitalizeFirstLetter(dataset.name)}</td>
                                                <td>{(new Date(dataset.created_at).toLocaleString('en-CA', { month: 'short', day: 'numeric', year: 'numeric' }))}</td>
                                                <td><a href={`/${projectId}/datasets/raw/${dataset.id}/view`} className="btn btn-outline-success btn-sm rounded-pill">View Dataset</a></td>
                                                <td><button type="button" className="btn btn-outline-success btn-sm rounded-pill" onClick={visualizeDataset} _id={dataset.id}>Visualize</button></td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table> : null}
                    </div>
                </div>
                <hr />
                <div className="row">
                    <div className="col-6">
                        <h4 className="header-title mb-0 h-100 d-flex align-items-center">Cleaned Datasets</h4>
                    </div>
                    <div className="col-6">
                        <button className="button-no-style float-end" title="Clean Raw Dataset" data-plugin="tippy" onClick={createNewCleanedDS}>
                            <i className="fe-plus noti-icon text-color btn-link"></i>
                        </button>
                    </div>
                </div>
                <div id="cardCollpase4" className="collapse pt-3 show">
                    <div className="table-responsive">
                        {cleanedDatasets !== null ?
                            <table className="table table-centered table-nowrap table-borderless mb-0">
                                <thead className="table-light">
                                    <tr>
                                        <th>Name</th>
                                        <th>Created At</th>
                                        <th>Rules</th>
                                        <th>Dataset</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {cleanedDatasets.map((dataset, index) => {
                                        return (
                                            <tr key={index}>
                                                <td>{window.capitalizeFirstLetter(dataset.name)}</td>
                                                <td>{(new Date(dataset.created_at).toLocaleString('en-CA', { month: 'short', day: 'numeric', year: 'numeric' }))}</td>
                                                <td><a href={`/${projectId}/datasets/${dataset.id}/rules`} className="btn btn-outline-warning btn-sm rounded-pill">View Rules</a></td>
                                                <td><a href={`/${projectId}/datasets/cleaned/${dataset.id}/view`} className="btn btn-outline-success btn-sm rounded-pill">View Dataset</a></td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table> : null}
                    </div>
                </div>
            </div>
            <GenericModal hideNext={false} />
        </div>
    );
}

export default Datasets;