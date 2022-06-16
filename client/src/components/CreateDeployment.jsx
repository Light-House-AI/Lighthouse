import React, { useEffect, useRef } from "react";

function CreateDeployment() {
    const selectModelsRef = useRef(null);

    useEffect(() => {
        window.$(selectModelsRef.current).select2();
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
                                    <label htmlFor="modelname" className="form-label">Deployment Name</label>
                                    <input type="text" id="modelname" className="form-control" placeholder="Enter deployment name" />
                                </div>
                                {/* CHAMPION-CHALLENGER / FALLOUT */}
                                <div className="mb-3">
                                    <label className="form-label">Project Type</label><br />
                                    <div className="form-check form-check-inline">
                                        <input type="radio" id="customRadio1" name="deploymenttype" className="form-check-input" defaultChecked />
                                        <label className="form-check-label" htmlFor="customRadio1">Champion-Challenger</label>
                                    </div>
                                    <div className="form-check form-check-inline">
                                        <input type="radio" id="customRadio2" name="deploymenttype" className="form-check-input" />
                                        <label className="form-check-label" htmlFor="customRadio2">Fallout</label>
                                    </div>
                                </div>
                            </div>
                            <div className="col-xl-6">
                                <div className="mb-3">
                                    <label htmlFor="models-select" className="form-label">Select Model(s)</label>
                                    <select id="models-select" ref={selectModelsRef} className="form-control select2-multiple" data-toggle="select2" data-width="100%" multiple="multiple" data-placeholder="Choose models...">
                                        <optgroup label="Alaskan/Hawaiian Time Zone">
                                            <option value="AK">Alaska</option>
                                            <option value="HI">Hawaii</option>
                                        </optgroup>
                                        <optgroup label="Pacific Time Zone">
                                            <option value="CA">California</option>
                                            <option value="NV">Nevada</option>
                                            <option value="OR">Oregon</option>
                                            <option value="WA">Washington</option>
                                        </optgroup>
                                        <optgroup label="Mountain Time Zone">
                                            <option value="AZ">Arizona</option>
                                            <option value="CO">Colorado</option>
                                            <option value="ID">Idaho</option>
                                            <option value="MT">Montana</option>
                                            <option value="NE">Nebraska</option>
                                            <option value="NM">New Mexico</option>
                                            <option value="ND">North Dakota</option>
                                            <option value="UT">Utah</option>
                                            <option value="WY">Wyoming</option>
                                        </optgroup>
                                        <optgroup label="Central Time Zone">
                                            <option value="AL">Alabama</option>
                                            <option value="AR">Arkansas</option>
                                            <option value="IL">Illinois</option>
                                            <option value="IA">Iowa</option>
                                            <option value="KS">Kansas</option>
                                            <option value="KY">Kentucky</option>
                                            <option value="LA">Louisiana</option>
                                            <option value="MN">Minnesota</option>
                                            <option value="MS">Mississippi</option>
                                            <option value="MO">Missouri</option>
                                            <option value="OK">Oklahoma</option>
                                            <option value="SD">South Dakota</option>
                                            <option value="TX">Texas</option>
                                            <option value="TN">Tennessee</option>
                                            <option value="WI">Wisconsin</option>
                                        </optgroup>
                                        <optgroup label="Eastern Time Zone">
                                            <option value="CT">Connecticut</option>
                                            <option value="DE">Delaware</option>
                                            <option value="FL">Florida</option>
                                            <option value="GA">Georgia</option>
                                            <option value="IN">Indiana</option>
                                            <option value="ME">Maine</option>
                                            <option value="MD">Maryland</option>
                                            <option value="MA">Massachusetts</option>
                                            <option value="MI">Michigan</option>
                                            <option value="NH">New Hampshire</option>
                                            <option value="NJ">New Jersey</option>
                                            <option value="NY">New York</option>
                                            <option value="NC">North Carolina</option>
                                            <option value="OH">Ohio</option>
                                            <option value="PA">Pennsylvania</option>
                                            <option value="RI">Rhode Island</option>
                                            <option value="SC">South Carolina</option>
                                            <option value="VT">Vermont</option>
                                            <option value="VA">Virginia</option>
                                            <option value="WV">West Virginia</option>
                                        </optgroup>
                                    </select>
                                </div>
                                {/* CREATE / CANCEL */}
                                <div className="row float-end">
                                    <div className="col-12 text-center">
                                        <button type="button" className="btn btn-light waves-effect waves-light m-1"><i className="fe-x me-1"></i>Cancel</button>
                                        <button type="button" className="btn btn-success waves-effect waves-light m-1"><i className="fe-check-circle me-1"></i>Create</button>
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

export default CreateDeployment;