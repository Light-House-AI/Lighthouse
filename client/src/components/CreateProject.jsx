import React, { useRef } from "react";

function CreateProject() {
    const inputFile = useRef(null);

    const openFile = function () {
        inputFile.current.click();
    }
    return (
        <div className="row">
            <div className="col-12">
                <div className="card">
                    <div className="card-body">
                        <div className="row">
                            <div className="col-xl-6">
                                {/* PROJECT NAME */}
                                <div className="mb-3">
                                    <label htmlFor="projectname" className="form-label">Project Name</label>
                                    <input type="text" id="projectname" className="form-control" placeholder="Enter project name" />
                                </div>
                                {/* PROJECT DESCRIPTION */}
                                <div className="mb-3">
                                    <label htmlFor="project-overview" className="form-label">Project Overview</label>
                                    <textarea className="form-control" id="project-overview" rows="5" placeholder="Enter some brief about project.."></textarea>
                                </div>
                                {/* REGRESSION / CLASSIFICATION */}
                                <div className="mb-3">
                                    <label className="form-label">Project Type</label> <br />
                                    <div className="form-check form-check-inline">
                                        <input type="radio" id="customRadio1" name="projecttype" className="form-check-input" />
                                        <label className="form-check-label" htmlFor="customRadio1">Regression</label>
                                    </div>
                                    <div className="form-check form-check-inline">
                                        <input type="radio" id="customRadio2" name="projecttype" className="form-check-input" defaultChecked />
                                        <label className="form-check-label" htmlFor="customRadio2">Classification</label>
                                    </div>
                                </div>
                            </div>
                            {/* Upload CSV */}
                            <div className="col-xl-6">
                                <div className="my-3 mt-xl-0">
                                    <label htmlFor="projectname" className="mb-0 form-label">Upload Dataset</label>
                                    <p className="text-muted font-14">Supported file extension .csv</p>
                                    <div className="dropzone" onClick={openFile}>
                                        <div className="fallback">
                                            <input ref={inputFile} name="file" type="file" className="d-none" accept=".csv" />
                                        </div>
                                        <div className="dz-message needsclick">
                                            <i className="h3 text-muted dripicons-cloud-upload"></i>
                                            <h4>Drop files here or click to upload.</h4>
                                        </div>
                                    </div>
                                </div>
                                {/* Dataset Output column */}
                                <div className="mb-3">
                                    <label htmlFor="project-budget" className="form-label">Dataset output column</label>
                                    <input type="text" id="project-budget" className="form-control" placeholder="Enter output column name" />
                                </div>
                                {/* CREATE / CANCEL */}
                                <div className="row float-end">
                                    <div className="col-12 text-center">
                                        <button type="button" className="btn btn-light waves-effect waves-light m-1"><i className="fe-x me-1"></i>Cancel</button>
                                        <button type="button" className="btn btn-success waves-effect waves-light m-1"><i className="fe-arrow-right me-1"></i>Next</button>
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

export default CreateProject;