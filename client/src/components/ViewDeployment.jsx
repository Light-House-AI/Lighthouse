import React, { useState, useEffect, useRef } from "react";

function ViewDeployment(props) {
    const [deploymentDetails] = useState(props.deploymentDetails);
    const selectModelsRef = useRef(null);
    const selectModelsRef2 = useRef(null);

    useEffect(() => {
        window.selectSecondaryModels = window.$(selectModelsRef.current).selectize({
            maxItems: 1
        });
        window.selectSecondaryModels = window.$(selectModelsRef2.current).selectize({
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
                                {/* DEPLOYMENT NAME */}
                                <div className="mb-3">
                                    <label htmlFor="deployment-name" className="form-label">Deployment Name:</label>
                                    <input type="text" id="deployment-name" className="form-control" value={window.capitalizeFirstLetter(deploymentDetails.name)} disabled />
                                </div>
                                {/* CHAMPION-CHALLENGER / CHAMPION */}
                                <div className="mb-3">
                                    <label className="form-label">Deployment Type:</label><br />
                                    <div className="form-check form-check-inline">
                                        <input type="radio" id="customRadio1" name="deploymenttype" className="form-check-input" defaultChecked={deploymentDetails.type === 'champion_challenger' ? true : false} disabled />
                                        <label className="form-check-label" htmlFor="customRadio1">Champion-Challenger</label>
                                    </div>
                                    <div className="form-check form-check-inline">
                                        <input type="radio" id="customRadio2" name="deploymenttype" className="form-check-input" defaultChecked={deploymentDetails.type !== 'champion_challenger' ? true : false} disabled />
                                        <label className="form-check-label" htmlFor="customRadio2">Single Model</label>
                                    </div>
                                </div>
                            </div>
                            <div className="col-xl-6">
                                <div className="mb-3">
                                    <label htmlFor="models-select" className="form-label">Select Primary Model:</label>
                                    <select id="models-select" ref={selectModelsRef} disabled>
                                        <option>{deploymentDetails.primary_model.name}</option>
                                    </select>
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="models-select" className="form-label">Select Secondary Model:</label>
                                    <select id="models-select" ref={selectModelsRef2} disabled>
                                        {deploymentDetails.secondary_model !== null ?
                                            <option>{deploymentDetails.secondary_model.name}</option> : null}
                                    </select>
                                </div>
                                {/* ENABLE/DISABLE DEPLOYMENT */}
                                <div className="mb-3">
                                    <label className="form-label">Status:</label><br />
                                    <div className="form-check form-check-inline">
                                        <input type="radio" id="customRadio1" name="deployment-action" className="form-check-input" defaultChecked={deploymentDetails.is_running ? true : false} disabled />
                                        <label className="form-check-label" htmlFor="customRadio1">Enable</label>
                                    </div>
                                    <div className="form-check form-check-inline">
                                        <input type="radio" id="customRadio2" name="deployment-action" className="form-check-input" defaultChecked={!deploymentDetails.is_running ? true : false} disabled />
                                        <label className="form-check-label" htmlFor="customRadio2">Disable</label>
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

export default ViewDeployment;