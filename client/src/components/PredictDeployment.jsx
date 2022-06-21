import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

function PredictDeployment(props) {
    const [projectDetails] = useState(props.projectDetails);
    const [deploymentDetails] = useState(props.deploymentDetails);
    const [columns] = useState(props.columns);
    const selectModelsRef = useRef(null);

    useEffect(() => {
        window.activateHorizontalScroll();
    }, []);

    const predictModelDeployment = () => {
        document.getElementById('error-div').classList.add('d-none');
        document.getElementById('predicted_value').value = "";

        let columns_value = {};
        for (let i = 0; i < columns.length; i++) {
            columns_value[columns[i]] = window.$(`input[name=${columns[i]}]`).val()
        }

        axios.post(`/deployments/${deploymentDetails.id}/predict`, columns_value, {
            headers: {
                "Content-Type": "application/json",
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            document.getElementById('predicted_value').value = response.data;
        }).catch((error) => {
            if (error.response.status === 400 || error.response.status === 404) {
                document.getElementById('error-message').innerHTML = error.response.data.error;
                document.getElementById('error-div').classList.remove('d-none');
            }
        });
    };

    return (
        <div className="card card-width-fixed mx-2 prediction">
            <div className="card-body d-inline">
                <label className="mb-1">Columns can have empty values.</label>
                <div className="table-responsive overflow-x-scroll">
                    <table className="table align-middle table-centered table-nowrap table-borderless mb-0">
                        <thead className="table-light">
                            <tr>
                                {columns !== null ?
                                    columns.map((column, index) => {
                                        return (
                                            <th key={index} className={projectDetails.predicted_column === column ? 'text-warning' : ''}>{projectDetails.predicted_column === column ? `PREDICTED ${window.capitalizeFirstLetter(column)}` : window.capitalizeFirstLetter(column)}</th>
                                        )
                                    })
                                    : null}
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                {columns !== null ?
                                    columns.map((column, index) => {
                                        return (
                                            <th key={index}>
                                                {projectDetails.predicted_column === column ?
                                                    <input id="predicted_value" type="text" name={column} className="form-control min-width-predict border-warning" disabled /> :
                                                    <input type="text" name={column} className="form-control min-width-predict" />}
                                            </th>
                                        )
                                    })
                                    : null}
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div className="row mt-2">
                    <div className="col-4 mt-1">
                        <div id='error-div' className="d-none">
                            <label id="error-msg" className="text-danger">Predicted Value:</label>
                        </div>
                    </div>
                    <div className="col-8 text-center d-flex justify-content-end">
                        <button type="button" className="btn btn-light waves-effect waves-light m-1"><i className="fe-x me-1"></i>Cancel</button>
                        <button type="button" className="btn btn-success waves-effect waves-light m-1" onClick={predictModelDeployment}><i className="fe-check-circle me-1"></i>Predict</button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default PredictDeployment;