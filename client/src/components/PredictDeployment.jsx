import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

function PredictDeployment(props) {
    const [projectDetails] = useState(props.projectDetails);
    const [deploymentDetails] = useState(props.deploymentDetails);
    const [columns, setColumns] = useState(props.columns);
    const selectModelsRef = useRef(null);

    useEffect(() => {
        window.predictionIndex = 1;
        window.activateHorizontalScroll();
        if (deploymentDetails.type !== 'single_model') {
            window.predictionIndex = 0;
            let newColumns = []
            for (let i = 0; i < columns.length; i++) {
                newColumns.push(columns[i])
                if (columns[i] === projectDetails.predicted_column) {
                    newColumns.push(columns[i]);
                }
            }
            setColumns(newColumns);
        }
    }, []);

    const predictModelDeployment = () => {
        document.getElementById('error-div').classList.add('d-none');
        document.getElementsByClassName('predicted_value')[0].value = "";
        if (deploymentDetails.type !== 'single_model')
            document.getElementsByClassName('predicted_value')[1].value = "";


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
            debugger
            document.getElementsByClassName('predicted_value')[0].value = response.data.primary_prediction;
            if (deploymentDetails.type !== 'single_model')
                document.getElementsByClassName('predicted_value')[1].value = response.data.secondary_prediction;
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
                                        if (projectDetails.predicted_column === column && deploymentDetails.type !== 'single_model')
                                            window.predictionIndex += 1;
                                        console.log(window.predictionIndex)
                                        return (
                                            <th key={index} className={projectDetails.predicted_column === column ? 'text-warning' : ''}>
                                                {projectDetails.predicted_column === column ? `${window.predictionIndex === 1 || window.predictionIndex === undefined ? `Primary` : `Secondary`} ${window.capitalizeFirstLetter(column)}` : window.capitalizeFirstLetter(column)}
                                            </th>
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
                                            <td key={index}>
                                                {projectDetails.predicted_column === column ?
                                                    <input type="text" name={column} className="form-control min-width-predict border-warning predicted_value" disabled /> :
                                                    <input type="text" name={column} className="form-control min-width-predict" />}
                                            </td>
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
                        <a href={`/${projectDetails.id}/deployments`} className="btn btn-light waves-effect waves-light m-1"><i className="fe-x me-1"></i>Cancel</a>
                        <button type="button" className="btn btn-success waves-effect waves-light m-1" onClick={predictModelDeployment}><i className="fe-check-circle me-1"></i>Predict</button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default PredictDeployment;