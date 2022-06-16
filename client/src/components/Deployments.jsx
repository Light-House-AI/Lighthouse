import React, { useEffect } from "react";

function Deployments() {
    useEffect(() => {
        window.$("#testing").footable();
    }, []);
    return (
        <div className="row">
            <div className="col-12">
                <div className="row">
                    <div className="col-6">
                        <h4 className="header-title mb-0 h-100 d-flex align-items-center">All Deployments</h4>
                    </div>
                    <div className="col-6">
                        <button className="button-no-style float-end" title="Add new deployment" data-plugin="tippy">
                            <i className="fe-plus noti-icon text-color btn-link"></i>
                        </button>
                    </div>
                </div>
                <div className="table-responsive pt-3">
                    <table id="testing" className="table table-centered table-nowrap table-borderless mb-0" data-sort="false">
                        <thead className="table-light">
                            <tr>
                                <th data-toggle="true">Name</th>
                                <th>Created At</th>
                                <th>Type</th>
                                <th>Status</th>
                                <th>Monitoring</th>
                                <th data-hide="all">Models</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>App design and development</td>
                                <td>Jan 03, 2015</td>
                                <td><span className="badge bg-soft-info text-info p-1">Champion - Challenger</span></td>
                                <td><span className="badge bg-soft-success text-success p-1">Active</span></td>
                                <td><button className="btn btn-outline-success btn-sm rounded-pill">View</button></td>
                                <td>Model 1</td>
                            </tr>
                            <tr>
                                <td>Coffee detail page - Main Page</td>
                                <td>Sep 21, 2016</td>
                                <td><span className="badge bg-soft-warning text-warning p-1">Fallout</span></td>
                                <td><span className="badge bg-soft-success text-success p-1">Active</span></td>
                                <td><button className="btn btn-outline-success btn-sm rounded-pill">View</button></td>
                                <td>Model 2</td>
                            </tr>
                            <tr>
                                <td>Poster illustation design</td>
                                <td>Mar 08, 2018</td>
                                <td><span className="badge bg-soft-info text-info p-1">Champion - Challenger</span></td>
                                <td><span className="badge bg-soft-danger text-danger p-1">Disabled</span></td>
                                <td><button className="btn btn-outline-success btn-sm rounded-pill disabled">View</button></td>
                                <td>Model 1, Model 2</td>
                            </tr>
                            <tr>
                                <td>Coffee detail page - Main Page</td>
                                <td>Sep 21, 2016</td>
                                <td><span className="badge bg-soft-warning text-warning p-1">Fallout</span></td>
                                <td><span className="badge bg-soft-danger text-danger p-1">Disabled</span></td>
                                <td><button className="btn btn-outline-success btn-sm rounded-pill disabled">View</button></td>
                                <td>Model 2</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default Deployments;