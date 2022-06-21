import React, { useState } from "react";

function ViewModel(props) {
    const [modelDetails] = useState(props.modelDetails);
    const [type] = useState(props.type);

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
                                    <input type="text" id="model-name" className="form-control" value={window.capitalizeFirstLetter(modelDetails.name)} disabled />
                                </div>
                                {/* NUMBER OF LAYERS */}
                                <div className="mb-2">
                                    <label className="form-label mb-0">Number of layers: (Optional)</label><br />
                                    <small className="text-muted">CSV: 3,4,5</small>
                                    <input type="text" className="form-control" id='model-layers' value={modelDetails.number_of_layers} disabled />
                                </div>
                                {/* MAXIMUM NEURONS PER LAYER */}
                                <div className="mb-2">
                                    <label className="form-label mb-0">Maximum neurons/layer: (Optional)</label><br />
                                    <small className="text-muted">CSV: 128,64,32,16,8</small>
                                    <input type="text" className="form-control" id='model-neurons' value={modelDetails.maximum_neurons_per_layer} disabled />
                                </div>
                            </div>
                            <div className="col-xl-6">
                                {/* LEARNING RATE */}
                                <div className="mb-2">
                                    <label className="form-label mb-0">Learning Rate: (Optional)</label><br />
                                    <small className="text-muted">CSV: 0.001,0.01,0.1,0.5,1</small>
                                    <input type="text" className="form-control" id='model-rate' value={modelDetails.learning_rate} disabled />
                                </div>
                                {/* BATCH SIZE */}
                                <div className="mb-2">
                                    <label className="form-label mb-0">Batch size: (Optional)</label><br />
                                    <small className="text-muted">CSV: 1,2,4,8,16,32,64</small>
                                    <input type="text" className="form-control" id='model-batch' value={modelDetails.batch_size} disabled />
                                </div>
                                {/* METRIC */}
                                {type === 'classification' ?
                                    <div className="mb-2">
                                        <label className="form-label mb-0">Metric (Accuracy):</label><br />
                                        <input type="text" className="form-control" id='model-batch' value={modelDetails.accuracy_score === null ? `null` : modelDetails.accuracy_score} disabled />
                                    </div> :
                                    <div className="mb-2">
                                        <label className="form-label mb-0">Metric (MSE):</label><br />
                                        <input type="text" className="form-control" id='model-batch' value={modelDetails.mean_squared_log_error === null ? `null` : modelDetails.mean_squared_log_error} disabled />
                                    </div>}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ViewModel;