import React, { useRef } from "react";
import axios from "axios";

function CreateProject() {
    const inputFile = useRef(null);

    const openFile = function () {
        inputFile.current.click();
    }

    const addProject = function () {
        document.getElementById('error-div').classList.add('d-none');
        document.getElementById('next-btn').classList.add('disabled');
        window.$("#loading-btn").html('<div class="spinner-border spinner-border-sm text-white me-1" role="status"></div>');
        const project_data = {
            name: document.getElementById("project-name").value,
            overview: document.getElementById("project-overview").value,
            type: document.querySelector('input[name="projecttype"]:checked').value,
            predicted_column: document.getElementById("predicted-column").value
        }

        if (project_data.name === "" || project_data.predicted_column === "" ||
            document.getElementById('dataset-name').value === "" || inputFile.current.files.length === 0) {
            if (project_data.name === "") {
                document.getElementById('error-msg').innerHTML = "Project name is required";
            }
            else if (project_data.predicted_column === "") {
                document.getElementById('error-msg').innerHTML = "Output column is required";
            }
            else if (document.getElementById('dataset-name').value === "") {
                document.getElementById('error-msg').innerHTML = "Dataset name is required";
            }
            else if (inputFile.current.files.length === 0) {
                document.getElementById('error-msg').innerHTML = "Upload a dataset file";
            }
            document.getElementById('error-div').classList.remove('d-none');
            document.getElementById('next-btn').classList.remove('disabled');
            window.$("#loading-btn").html('<i class="fe-arrow-right me-1"></i>');
            return;
        }

        axios.post("/projects/", project_data, {
            headers: {
                "Content-Type": "application/json",
                "Authorization": localStorage.getItem("tokenType") + " " + localStorage.getItem("accessToken")
            }
        }).then((res_proj) => {
            // create dataset
            const dataset_data = {
                project_id: res_proj.data.id,
                name: document.getElementById('dataset-name').value,
                creation_method: "upload"
            }
            axios.post('/raw_datasets', dataset_data, {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": localStorage.getItem("tokenType") + " " + localStorage.getItem("accessToken")
                }
            }).then((res_dataset) => {
                // upload file
                const formData = new FormData();
                formData.append('file', inputFile.current.files[0]);
                axios.post(`/raw_datasets/${res_dataset.data.id}/upload`, formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                        "Authorization": localStorage.getItem("tokenType") + " " + localStorage.getItem("accessToken")
                    }
                }).then((response) => {
                    // go to rules page
                    // /:projectid/datasets/:datasetid/clean
                    window.location.href = `/${res_proj.data.id}/datasets/${res_dataset.data.id}/clean`;
                }).catch((error) => {
                    document.getElementById('next-btn').classList.remove('disabled');
                    window.$("#loading-btn").html('<i class="fe-arrow-right me-1"></i>');
                    if (error.response.status === 401) {
                        localStorage.clear();
                        window.location.href = "/login";
                    }
                    if (error.response.status === 404) {
                        document.getElementById('error-msg').innerHTML = "Something went wrong. Please try again.";
                        document.getElementById('error-div').classList.remove('d-none');
                    }
                });
            }).catch((error) => {
                document.getElementById('next-btn').classList.remove('disabled');
                window.$("#loading-btn").html('<i class="fe-arrow-right me-1"></i>');
                if (error.response.status === 401) {
                    localStorage.clear();
                    window.location.href = "/login";
                }
            });
        }).catch((err) => {
            document.getElementById('next-btn').classList.remove('disabled');
            window.$("#loading-btn").html('<i class="fe-arrow-right me-1"></i>');
            if (err.response.status === 401) {
                localStorage.clear();
                window.location.href = "/login";
            }
        });
    }

    const cancelProject = function () {
        window.location.href = "/";
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
                                    <label htmlFor="project-name" className="form-label">Project Name</label>
                                    <input type="text" id="project-name" className="form-control" placeholder="Enter project name" />
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
                                        <input type="radio" id="customRadio1" name="projecttype" className="form-check-input" value="regression" />
                                        <label className="form-check-label" htmlFor="customRadio1">Regression</label>
                                    </div>
                                    <div className="form-check form-check-inline">
                                        <input type="radio" id="customRadio2" name="projecttype" className="form-check-input" defaultChecked value="classification" />
                                        <label className="form-check-label" htmlFor="customRadio2">Classification</label>
                                    </div>
                                </div>
                                {/* CREATE / CANCEL / ERROR */}
                                <div className="row float-end">
                                    <div className="col-12 text-center">
                                        <a href={`/`} className="btn btn-light waves-effect waves-light m-1" onClick={cancelProject}><i className="fe-x me-1"></i>Cancel</a>
                                        <button id="next-btn" type="button" className="btn btn-success waves-effect waves-light m-1" onClick={addProject}>
                                            <div id="loading-btn" className="d-inline">
                                                <i className="fe-arrow-right me-1"></i>
                                            </div>Next
                                        </button>
                                    </div>
                                </div>
                                {/* ERROR DIV */}
                                <div id="error-div" className="d-none mt-4">
                                    <label id="error-msg" className="text-danger"></label>
                                </div>
                            </div>
                            <div className="col-xl-6">
                                {/* RAW DATASET NAME */}
                                <div className="mb-3">
                                    <label htmlFor="dataset-name" className="form-label">Dataset Name</label>
                                    <input type="text" id="dataset-name" className="form-control" placeholder="Enter dataset name for versioning" />
                                </div>
                                {/* Upload CSV */}
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
                                    <label htmlFor="predicted-column" className="form-label">Dataset output column</label>
                                    <input type="text" id="predicted-column" className="form-control" placeholder="Enter output column name" />
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