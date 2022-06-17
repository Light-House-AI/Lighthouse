import axios from "axios";
import React, { useState } from "react";

function CreateModel(props) {
    const [projectId] = useState(props.projectId);
    const [cleanedDatasetId] = useState(props.cleanedDatasetId);
    const [isPipeline] = useState(props.isPipeline);

    const modelCreation = function () {
        document.getElementById('error-div').classList.add('d-none');

        document.getElementById('next-btn').classList.add('disabled');
        window.$("#loading-btn").html('<div class="spinner-border spinner-border-sm text-white me-1" role="status"></div>');

        if (document.getElementById("model-name").value === '') {
            document.getElementById('error-msg').innerHTML = 'Model name is required.';
            document.getElementById('error-div').classList.remove('d-none');
            document.getElementById('next-btn').classList.remove('disabled');
            if (isPipeline)
                window.$("#loading-btn").html('<i class="fe-arrow-right me-1"></i>');
            else
                window.$("#loading-btn").html('<i class="fe-check-circle me-1"></i>');
            return;
        }

        var model_data = {
            project_id: projectId,
            dataset_id: cleanedDatasetId,
            name: document.getElementById("model-name").value
        }

        if (document.getElementById("model-layers").value.trim() !== '')
            model_data.number_of_layers = convertStringToArray(document.getElementById("model-layers").value.trim(), 'int');

        if (document.getElementById("model-neurons").value.trim() !== '')
            model_data.maximum_neurons_per_layer = convertStringToArray(document.getElementById("model-neurons").value.trim(), 'int');

        if (document.getElementById("model-rate").value.trim() !== '')
            model_data.learning_rate = convertStringToArray(document.getElementById("model-rate").value.trim(), 'float');

        if (document.getElementById("model-batch").value.trim() !== '')
            model_data.batch_size = convertStringToArray(document.getElementById("model-batch").value.trim(), 'int');

        axios.post('/models', model_data, {
            headers: {
                "Content-Type": "application/json",
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            window.location.href = `/${projectId}/deployments/${response.data.id}/create`;
        }).catch((error) => {
            if (isPipeline)
                window.$("#loading-btn").html('<i class="fe-arrow-right me-1"></i>');
            else
                window.$("#loading-btn").html('<i class="fe-check-circle me-1"></i>');
            document.getElementById('next-btn').classList.remove('disabled');
        });
    }

    const convertStringToArray = function (str, type = 'int') {
        var arr = str.split(',');
        var int_arr = [];
        for (var i = 0; i < arr.length; i++) {
            if (type === 'int')
                int_arr.push(parseInt(arr[i].trim()));
            else
                int_arr.push(parseFloat(arr[i].trim()));
        }
        return int_arr;
    }

    return (
        <div className="row">
            <div className="col-12">
                <div className="card">
                    <div className="card-body">
                        <div className="row">
                            <div className="col-xl-6">
                                {/* MODEL NAME */}
                                <div className="mb-2">
                                    <label htmlFor="modelname" className="form-label">Model Name:</label>
                                    <input type="text" id="model-name" className="form-control" placeholder="Enter model name" />
                                </div>
                                {/* NUMBER OF LAYERS */}
                                <div className="mb-2">
                                    <label className="form-label mb-0">Number of layers: (Optional)</label><br />
                                    <small className="text-muted">CSV: 3,4,5</small>
                                    <input type="text" className="form-control" id='model-layers' placeholder="3,4,5" />
                                </div>
                                {/* MAXIMUM NEURONS PER LAYER */}
                                <div className="mb-2">
                                    <label className="form-label mb-0">Maximum neurons/layer: (Optional)</label><br />
                                    <small className="text-muted">CSV: 128,64,32,16,8</small>
                                    <input type="text" className="form-control" id='model-neurons' placeholder="128,64,32,16,8" />
                                </div>
                            </div>
                            <div className="col-xl-6">
                                {/* LEARNING RATE */}
                                <div className="mb-2">
                                    <label className="form-label mb-0">Learning Rate: (Optional)</label><br />
                                    <small className="text-muted">CSV: 0.001,0.01,0.1,0.5,1</small>
                                    <input type="text" className="form-control" id='model-rate' placeholder="0.001,0.01,0.1,0.5,1" />
                                </div>
                                {/* BATCH SIZE */}
                                <div className="mb-2">
                                    <label className="form-label mb-0">Batch size: (Optional)</label><br />
                                    <small className="text-muted">CSV: 1,2,4,8,16,32,64</small>
                                    <input type="text" className="form-control" id='model-batch' placeholder="1,2,4,8,16,32,64" />
                                </div>
                                {/* CREATE / CANCEL */}
                                <div className="mb-2">
                                    <div className="row">
                                        <div className="col-md-5">
                                            <div id='error-div' className="mt-2 d-none">
                                                <label id="error-msg" className="text-danger"></label>
                                            </div>
                                        </div>
                                        <div className="col-md-7">
                                            <div className="row float-end">
                                                <div className="col-12 text-center">
                                                    <button type="button" className="btn btn-light waves-effect waves-light m-1"><i className="fe-x me-1"></i>Cancel</button>
                                                    {isPipeline === false ?
                                                        <button id="next-btn" type="button" className="btn btn-success waves-effect waves-light m-1" onClick={modelCreation}>
                                                            <div id="loading-btn" className="d-inline">
                                                                <i className="fe-check-circle me-1"></i>
                                                            </div>
                                                            Create
                                                        </button> :
                                                        <button id="next-btn" type="button" className="btn btn-success waves-effect waves-light m-1" onClick={modelCreation}>
                                                            <div id="loading-btn" className="d-inline">
                                                                <i className="fe-arrow-right me-1"></i>
                                                            </div>Next
                                                        </button>
                                                    }


                                                </div>
                                            </div>
                                        </div>
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

export default CreateModel;