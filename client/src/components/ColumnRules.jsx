import React, { useRef, useEffect, useState } from "react";

function ColumnRules(props) {
    const columnType = useRef(null);
    const columnFill = useRef(null);
    const [recommendation] = useState(props.recommendation);
    const [is_numeric, setIsNumeric] = useState(props.recommendation.is_numeric);
    const [is_nominal, setIsNominal] = useState(props.recommendation.is_nominal);
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

    const toggleNumeric = function () {
        setIsNumeric(!is_numeric);
    }

    const toggleNominal = function () {
        setIsNominal(!is_nominal);
    }

    return (
        <div className="card card-width-fixed mx-2">
            {recommendation !== null ?
                <div className="card-body">
                    {/* COLUMN NAME */}
                    <div className="mb-2">
                        <label className="form-label">Column Name:</label>
                        <input type="text" className="form-control" defaultValue={recommendation.column_name} disabled />
                    </div>
                    {/* DROP COLUMN */}
                    <div className="mb-2">
                        <div className="form-check form-switch">
                            <input className="form-check-input" type="checkbox" role="switch" defaultChecked={false} />
                            <label className="form-check-label">Drop column?</label>
                        </div>
                    </div>
                    {/* CATEGORICAL */}
                    <div className="mb-2" title={"Suggested: " + !recommendation.is_numeric} data-plugin="tippy">
                        <div className="form-check form-switch">
                            <input className="form-check-input" type="checkbox" role="switch" defaultChecked={!recommendation.is_numeric} onChange={toggleNumeric} />
                            <label className="form-check-label">Is categorical?</label>
                        </div>
                    </div>
                    {/* COLUMN TYPE */}
                    <div className="mb-2">
                        <label className="form-label">Column Type:</label>
                        <select ref={columnType} defaultValue={recommendation.datatype}>
                            <option value="object">object</option>
                            <option value="int64">int64</option>
                            <option value="float64">float64</option>
                            <option value="uint8">uint8</option>
                        </select>
                    </div>
                    {/* MINIMUM VALUE */}
                    <div className="mb-2">
                        <label className="form-label">Minimum Value:</label>
                        <input type="text" className="form-control" defaultValue={recommendation.min} disabled={!is_numeric} />
                    </div>
                    {/* MAXIMUM VALUE */}
                    <div className="mb-2">
                        <label className="form-label">Maximum Value:</label>
                        <input type="text" className="form-control" defaultValue={recommendation.max} disabled={!is_numeric} />
                    </div>
                    {/* AVERAGE/MODE VALUE */}
                    {recommendation.is_numeric ?
                        <div className="mb-2">
                            <label className="form-label">Mean Value:</label>
                            <input type="text" className="form-control" defaultValue={recommendation.mean} disabled />
                        </div> :
                        <div className="mb-2">
                            <label className="form-label">Mode Value:</label>
                            <input type="text" className="form-control" defaultValue={recommendation.mode} disabled />
                        </div>
                    }
                    {/* UNIQUE COUNTS */}
                    <div className="mb-2">
                        <label className="form-label">Unique Counts:</label>
                        <input type="text" className="form-control" defaultValue={recommendation.unique_count} disabled />
                    </div>
                    {/* UNIQUE VALUES */}
                    <div className="mb-2">
                        <label className="form-label">Unique Values:</label>
                        <input type="text" className="form-control" defaultValue={recommendation.unique_values} disabled={is_numeric} />
                    </div>
                    {/* FILL METHOD */}
                    <div className="mb-2">
                        <label className="form-label">Fill Method:</label>
                        <select ref={columnFill} defaultValue={recommendation.fill_method}>
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
                            <input className="form-check-input" type="checkbox" role="switch" defaultChecked={recommendation.is_nominal} onChange={toggleNominal} disabled={is_numeric} />
                            <label className="form-check-label">Is nominal?</label>
                        </div>
                    </div>
                    {/* ORDERLIST VALUES */}
                    <div className="mb-1">
                        <label className="form-label mb-0">Order Values:</label><br />
                        <small className="text-muted">CSV: 0,1,2</small>
                        <input type="text" className="form-control" placeholder="0,1,2" disabled={!is_numeric && !is_nominal ? true : false} />
                    </div>
                </div> : null}
        </div>
    );
}

export default ColumnRules;