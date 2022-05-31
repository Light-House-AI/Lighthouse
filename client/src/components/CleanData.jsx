import React from "react";

import ColumnRules from "./ColumnRules";

function CleanData() {

    return (
        <div className="row">
            <div className="col-12 mb-2">
                <div className="row float-end">
                    <div className="col-12 text-center">
                        <button type="button" className="btn btn-light waves-effect waves-light m-1"><i className="fe-x me-1"></i>Cancel</button>
                        <button type="button" className="btn btn-success waves-effect waves-light m-1"><i className="fe-check-circle me-1"></i>Create</button>
                    </div>
                </div>
            </div>
            <div className="col-12">
                <div className="row overflow-x-scroll enable-row-overflow-x me-1">
                    <ColumnRules />
                    <ColumnRules />
                    <ColumnRules />
                    <ColumnRules />
                    <ColumnRules />
                </div>
            </div>
        </div>
    );
}

export default CleanData;