import React, { useState, useEffect } from "react";
import axios from "axios";

function Datasets(props) {
    const [projectId] = useState(props.projectId);
    const [rawDatasets, setRawDatasets] = useState(null);
    const [cleanedDatasets, setCleanedDatasets] = useState(null);

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
    return (
        <div className="row">
            <div className="col-12">
                <div className="row">
                    <div className="col-6">
                        <h4 className="header-title mb-0 h-100 d-flex align-items-center">Raw Datasets</h4>
                    </div>
                    <div className="col-6">
                        <button className="button-no-style float-end" title="View/Add Shadow Data" data-plugin="tippy">
                            <i className="fe-plus noti-icon text-color btn-link"></i>
                        </button>
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
                                    </tr>
                                </thead>
                                <tbody>
                                    {rawDatasets.map((dataset, index) => {
                                        return (
                                            <tr key={index}>
                                                <td>{window.capitalizeFirstLetter(dataset.name)}</td>
                                                <td>{(new Date(dataset.created_at).toLocaleString('en-CA', { month: 'short', day: 'numeric', year: 'numeric' }))}</td>
                                                <td><a href={`/${projectId}/datasets/${dataset.id}/view`} className="btn btn-outline-success btn-sm rounded-pill">View Dataset</a></td>
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
                        <button className="button-no-style float-end" title="Clean Raw Dataset" data-plugin="tippy">
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
                                                <td><a href={`/${projectId}/datasets/${dataset.id}/view`} className="btn btn-outline-success btn-sm rounded-pill">View Dataset</a></td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table> : null}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Datasets;