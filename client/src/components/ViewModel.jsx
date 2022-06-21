import React, { useState, useRef, useEffect } from "react";

function ViewModel(props) {
    const [modelDetails] = useState(props.modelDetails);
    const [type] = useState(props.type);
    const selectDataset = useRef(null);

    useEffect(() => {
        window.selectSecondaryModels = window.$(selectDataset.current).selectize({
            maxItems: 1
        });
    }, []);

    return (
        <div className="row">
            <div className="col-12">
                <div className="card">
                    <div className="card-body">
                        <div className="row">
                            <div className="col-xl-6">
                                {/* MODEL NAME */}
                                <div className="row">
                                    <div className="col-6">
                                        <div className="mb-2">
                                            <label htmlFor="modelname" className="form-label">Model Name:</label>
                                            <input type="text" id="model-name" className="form-control" value={window.capitalizeFirstLetter(modelDetails.name)} disabled />
                                        </div>
                                    </div>
                                    <div className="col-6">
                                        <div className="mb-2">
                                            <label htmlFor="models-select" className="form-label">Cleaned Dataset Name:</label>
                                            <select id="models-select" ref={selectDataset} disabled>
                                                <option>{modelDetails.dataset.name}</option>
                                            </select>
                                        </div>
                                    </div>
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
                                        <input type="text" className="form-control" id='model-batch' value={modelDetails.score === null ? `-` : `${modelDetails.score * 100}%`} disabled />
                                    </div> :
                                    <div className="mb-2">
                                        <label className="form-label mb-0">Metric (MSLE):</label><br />
                                        <input type="text" className="form-control" id='model-batch' value={modelDetails.score === null ? `-` : modelDetails.score} disabled />
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