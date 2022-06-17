import React, { useRef, useEffect, useState } from "react";

function ViewRules(props) {
    const columnType = useRef(null);
    const columnFill = useRef(null);
    const [rules] = useState(props.rules);

    useEffect(() => {
        window.$(columnType.current).selectize({
            maxItems: 1
        });

        window.$(columnFill.current).selectize({
            maxItems: 1
        });

        window.tippy('[data-plugin="tippy"]', {
            placement: 'top',
            followCursor: 'false',
            arrow: 'true'
        });
    }, []);

    return (
        <div className="card card-width-fixed mx-2">
            {rules !== null ?
                <div className="card-body">
                    {/* COLUMN NAME */}
                    <div className="mb-2">
                        <label className="form-label">Column Name:</label>
                        <input type="text" className="form-control" defaultValue={rules.column_name} disabled />
                    </div>
                    {/* DROP COLUMN */}
                    <div className="mb-2">
                        <div className="form-check form-switch">
                            <input className="form-check-input" type="checkbox" role="switch" defaultChecked={false} disabled />
                            <label className="form-check-label">Drop column?</label>
                        </div>
                    </div>
                    {/* CATEGORICAL */}
                    <div className="mb-2">
                        <div className="form-check form-switch">
                            <input className="form-check-input" type="checkbox" role="switch" defaultChecked={!rules.is_numeric} disabled />
                            <label className="form-check-label">Is categorical?</label>
                        </div>
                    </div>
                    {/* COLUMN TYPE */}
                    <div className="mb-2">
                        <label className="form-label">Column Type:</label>
                        <select ref={columnType} defaultValue={rules.datatype} disabled>
                            <option value="object">object</option>
                            <option value="int64">int64</option>
                            <option value="float64">float64</option>
                            <option value="uint8">uint8</option>
                        </select>
                    </div>
                    {/* MINIMUM VALUE */}
                    <div className="mb-2">
                        <label className="form-label">Minimum Value:</label>
                        <input type="text" className="form-control" defaultValue={rules.min} disabled />
                    </div>
                    {/* MAXIMUM VALUE */}
                    <div className="mb-2">
                        <label className="form-label">Maximum Value:</label>
                        <input type="text" className="form-control" defaultValue={rules.max} disabled />
                    </div>
                    {/* AVERAGE/MODE VALUE */}
                    {rules.is_numeric ?
                        <div className="mb-2">
                            <label className="form-label">Mean Value:</label>
                            <input type="text" className="form-control" defaultValue={rules.mean} disabled name="mean" />
                        </div> :
                        <div className="mb-2">
                            <label className="form-label">Mode Value:</label>
                            <input type="text" className="form-control" defaultValue={rules.mode} disabled name="mode" />
                        </div>
                    }
                    {/* UNIQUE COUNTS */}
                    <div className="mb-2">
                        <label className="form-label">Unique Counts:</label>
                        <input type="text" className="form-control" value={rules.unique_count !== null ? rules.unique_count : ''} disabled />
                    </div>
                    {/* UNIQUE VALUES */}
                    <div className="mb-2">
                        <label className="form-label">Unique Values:</label>
                        <input type="text" className="form-control" defaultValue={rules.unique_values} disabled />
                    </div>
                    {/* FILL METHOD */}
                    <div className="mb-2">
                        <label className="form-label">Fill Method:</label>
                        <select ref={columnFill} defaultValue={rules.fill_method} name="fill_method" disabled>
                            <option value="">Select a fill method</option>
                            <option value="automatic">Automatic</option>
                            <option value="column">Drop Column</option>
                            <option value="row">Drop Row</option>
                            <option value="average">Average/Mode</option>
                            <option value="knn">KNN Impute</option>
                        </select>
                    </div>
                    {/* NOMINAL OR ORDINAL */}
                    <div className="mb-2">
                        <div className="form-check form-switch">
                            <input className="form-check-input" type="checkbox" role="switch" defaultChecked={rules.is_nominal} disabled />
                            <label className="form-check-label">Is nominal?</label>
                        </div>
                    </div>
                    {/* ORDERLIST VALUES */}
                    <div className="mb-1">
                        <label className="form-label mb-0">Order Values:</label><br />
                        <small className="text-muted">CSV: 0,1,2</small>
                        <input type="text" className="form-control" defaultValue={rules.ordinal_order} disabled />
                    </div>
                </div> : null}
        </div>
    );
}

export default ViewRules;