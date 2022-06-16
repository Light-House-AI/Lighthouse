import React from "react";

function CreateModel() {
    return (
        <div className="row">
            <div className="col-12">
                <div className="card">
                    <div className="card-body">
                        <div className="row">
                            <div className="col-xl-6">
                                {/* MODEL NAME */}
                                <div className="mb-3">
                                    <label htmlFor="modelname" className="form-label">Model Name</label>
                                    <input type="text" id="modelname" className="form-control" placeholder="Enter model name" />
                                </div>
                            </div>
                            <div className="col-xl-6">
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

export default CreateModel;