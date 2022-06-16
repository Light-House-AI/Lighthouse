import React, { useEffect, useRef } from "react";

function Models() {
    const tableRef = useRef(null);
    useEffect(() => {
        window.$(tableRef.current).footable();
    }, []);
    return (
        <div className="row">
            <div className="col-12">
                <div className="row">
                    <div className="col-6">
                        <h4 className="header-title mb-0 h-100 d-flex align-items-center">All Models</h4>
                    </div>
                    <div className="col-6">
                        <button className="button-no-style float-end" title="Add new model" data-plugin="tippy">
                            <i className="fe-plus noti-icon text-color btn-link"></i>
                        </button>
                    </div>
                </div>
                <div className="table-responsive pt-3">
                    <table ref={tableRef} className="table table-centered table-nowrap table-borderless mb-0" data-sort="false">
                        <thead className="table-light">
                            <tr>
                                <th data-toggle="true">Name</th>
                                <th>Created At</th>
                                <th>Status</th>
                                <th data-hide="all">Dataset names</th>
                                <th data-hide="all">Model parameters</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>App design and development</td>
                                <td>Jan 03, 2015</td>
                                <td><span className="badge bg-soft-success text-success p-1">Used</span></td>
                                <td>Dataset 1</td>
                                <td>None</td>
                            </tr>
                            <tr>
                                <td>Coffee detail page - Main Page</td>
                                <td>Sep 21, 2016</td>
                                <td><span className="badge bg-soft-warning text-warning p-1">Not used</span></td>
                                <td>Dataset 1, Dataset 2</td>
                                <td>None</td>
                            </tr>
                            <tr>
                                <td>Poster illustation design</td>
                                <td>Mar 08, 2018</td>
                                <td><span className="badge bg-soft-warning text-warning p-1">Not used</span></td>
                                <td>Dataset 2</td>
                                <td>None</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default Models;