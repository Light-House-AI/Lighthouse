import React, { useRef, useEffect } from "react";

function ColumnRules() {
    const columnType = useRef(null);
    const columnFill = useRef(null);

    useEffect(() => {
        window.$(columnType.current).selectize({
            maxItems: 1
        });

        window.$(columnFill.current).selectize({
            maxItems: 1
        });
    }, []);
    return (
        <div className="card card-width-fixed mx-2">
            <div className="card-body">
                {/* COLUMN NAME */}
                <div className="mb-2">
                    <label className="form-label">Column Name:</label>
                    <input type="text" className="form-control" disabled />
                </div>
                {/* CATEGORICAL */}
                <div className="mb-2">
                    <div className="form-check form-switch">
                        <input className="form-check-input" type="checkbox" role="switch" defaultChecked />
                        <label className="form-check-label">Categorical</label>
                    </div>
                </div>
                {/* COLUMN TYPE */}
                <div className="mb-2">
                    <label className="form-label">Column Type:</label>
                    <select ref={columnType}>
                        <option value="">Select column type</option>
                        <option value="AL">Alabama</option>
                    </select>
                </div>
                {/* MINIMUM VALUE */}
                <div className="mb-2">
                    <label className="form-label">Minimum Value:</label>
                    <input type="text" className="form-control" />
                </div>
                {/* MAXIMUM VALUE */}
                <div className="mb-2">
                    <label className="form-label">Maximum Value:</label>
                    <input type="text" className="form-control" />
                </div>
                {/* UNIQUE VALUES */}
                <div className="mb-2">
                    <label className="form-label">Unique Values:</label>
                    <input type="text" className="form-control" placeholder="" />
                </div>
                {/* UNIQUE COUNTS */}
                <div className="mb-2">
                    <label className="form-label">Unique Counts:</label>
                    <input type="text" className="form-control" />
                </div>
                {/* DROP VALUES */}
                <div className="mb-2">
                    <label className="form-label mb-0">Droplist Values:</label><br />
                    <small className="text-muted">CSV: 0,1,2</small>
                    <input type="text" className="form-control" />
                </div>
                {/* FILL METHOD */}
                <div className="mb-2">
                    <label className="form-label">Fill Method:</label>
                    <select ref={columnFill}>
                        <option value="">Select a fill method</option>
                        <option value="automatic">Automatic</option>
                        <option value="column">Drop Column</option>
                        <option value="row">Drop Row</option>
                        <option value="avg">Average/Mode</option>
                        <option value="knn">KNN Impute</option>
                    </select>
                </div>
                {/* NOMINAL OR ORDINAL */}
                <div className="mb-2">
                    <div className="form-check form-switch">
                        <input className="form-check-input" type="checkbox" role="switch" />
                        <label className="form-check-label">Nominal</label>
                    </div>
                </div>
                {/* ORDERLIST VALUES */}
                <div className="mb-1">
                    <label className="form-label mb-0">Order Values:</label><br />
                    <small className="text-muted">CSV: 0,1,2</small>
                    <input type="text" className="form-control" />
                </div>
            </div>
        </div>
    );
}

export default ColumnRules;