import React from "react";

function Datasets() {
    return (
        <div className="row">
            <div className="col-12">
                <div className="row">
                    <div className="col-6">
                        <h4 className="header-title mb-0 h-100 d-flex align-items-center">Raw Datasets</h4>
                    </div>
                    <div className="col-6">
                        <button className="button-no-style float-end" title="View/Add Shadow Data" data-plugin="tippy">
                            <i className="fe-plus noti-icon text-color btn-link"></i>
                        </button>
                    </div>
                </div>
                <div id="cardCollpase4" className="collapse pt-3 show">
                    <div className="table-responsive">
                        <table className="table table-centered table-nowrap table-borderless mb-0">
                            <thead className="table-light">
                                <tr>
                                    <th>Name</th>
                                    <th>Created At</th>
                                    <th>Dataset</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>App design and development</td>
                                    <td>Jan 03, 2015</td>
                                    <td><button className="btn btn-outline-success btn-sm rounded-pill">View Dataset</button></td>
                                </tr>
                                <tr>
                                    <td>Coffee detail page - Main Page</td>
                                    <td>Sep 21, 2016</td>
                                    <td><button className="btn btn-outline-success btn-sm rounded-pill">View Dataset</button></td>
                                </tr>
                                <tr>
                                    <td>Poster illustation design</td>
                                    <td>Mar 08, 2018</td>
                                    <td><button className="btn btn-outline-success btn-sm rounded-pill">View Dataset</button></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <hr />
                <div className="row">
                    <div className="col-6">
                        <h4 className="header-title mb-0 h-100 d-flex align-items-center">Cleaned Datasets</h4>
                    </div>
                    <div className="col-6">
                        <button className="button-no-style float-end" title="Clean Raw Dataset" data-plugin="tippy">
                            <i className="fe-plus noti-icon text-color btn-link"></i>
                        </button>
                    </div>
                </div>
                <div id="cardCollpase4" className="collapse pt-3 show">
                    <div className="table-responsive">
                        <table className="table table-centered table-nowrap table-borderless mb-0">
                            <thead className="table-light">
                                <tr>
                                    <th>Name</th>
                                    <th>Created At</th>
                                    <th>Rules</th>
                                    <th>Dataset</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>App design and development</td>
                                    <td>Jan 03, 2015</td>
                                    <td><button className="btn btn-outline-warning btn-sm rounded-pill">View Rules</button></td>
                                    <td><button className="btn btn-outline-success btn-sm rounded-pill">View Dataset</button></td>
                                </tr>
                                <tr>
                                    <td>Coffee detail page - Main Page</td>
                                    <td>Sep 21, 2016</td>
                                    <td><button className="btn btn-outline-warning btn-sm rounded-pill">View Rules</button></td>
                                    <td><button className="btn btn-outline-success btn-sm rounded-pill">View Dataset</button></td>
                                </tr>
                                <tr>
                                    <td>Poster illustation design</td>
                                    <td>Mar 08, 2018</td>
                                    <td><button className="btn btn-outline-warning btn-sm rounded-pill">View Rules</button></td>
                                    <td><button className="btn btn-outline-success btn-sm rounded-pill">View Dataset</button></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Datasets;