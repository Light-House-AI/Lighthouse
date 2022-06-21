import React, { useRef, useEffect, useState, useImperativeHandle } from "react";

function ColumnRules(props) {
    const columnType = useRef(null);
    const columnFill = useRef(null);
    const [recommendation] = useState(props.recommendation);
    const [rule, setRule] = useState(props.recommendation);
    const [statistics] = useState(props.statistics);
    const [is_numeric, setIsNumeric] = useState(props.recommendation.is_numeric);
    const [is_nominal, setIsNominal] = useState(props.recommendation.is_nominal);
    const [dropColumn, setDropColumn] = useState(false);
    const [prevFillMethod, setPrevFillMethod] = useState(props.recommendation.fill_method)
    const [uniqueCount, setUniqueCount] = useState(recommendation.unique_count != null ? recommendation.unique_count.toString() : '');

    useEffect(() => {
        setRule({ ...rule, unique_values: rule.unique_values === '' ? null : rule.unique_values.split(',') });

        window.selectType = window.$(columnType.current).selectize({
            maxItems: 1,
            onChange: function (value) {
                setRule({ ...rule, [window.$(this)[0].$input[0].name]: value });
            }
        });

        window.selectFill = window.$(columnFill.current).selectize({
            maxItems: 1,
            onChange: function (value) {
                setRule({ ...rule, [window.$(this)[0].$input[0].name]: value });
                setPrevFillMethod(value);
            }
        });

        window.tippy('[data-plugin="tippy"]', {
            placement: 'top',
            followCursor: 'false',
            arrow: 'true'
        });
    }, []);

    useEffect(() => {
        if (window.selectType !== undefined && window.selectType !== null) {
            if (dropColumn)
                window.selectType[0].selectize.disable();
            else
                window.selectType[0].selectize.enable();
        }

        if (window.selectFill !== undefined && window.selectFill !== null) {
            if (dropColumn)
                window.selectFill[0].selectize.disable();
            else
                window.selectFill[0].selectize.enable();
        }
    }, [dropColumn])

    const toggleDropColumn = function () {
        if (!dropColumn)
            setRule({ ...rule, fill_method: 'column' });
        else
            setRule({ ...rule, fill_method: prevFillMethod });
        setDropColumn(!dropColumn);
    }

    const toggleNumeric = function (e) {
        setIsNumeric(!is_numeric);
        restructureRule(e);
    }

    const toggleNominal = function (e) {
        setIsNominal(!is_nominal);
        restructureRule(e);
    }

    const restructureRule = (e) => {
        if (e.target.type === 'checkbox' && e.target.name === 'is_numeric') {
            setRule({ ...rule, [e.target.name]: (e.target.checked === 'on' || e.target.checked === true || e.target.checked === 'true') ? false : true });
        }
        else if (e.target.type === 'checkbox' && e.target.name === 'is_nominal') {
            setRule({ ...rule, [e.target.name]: (e.target.checked === 'on' || e.target.checked === true || e.target.checked === 'true') ? true : false });
        }
        else if (e.target.name === 'unique_values') {
            var uniqueValues = e.target.value.split(',');
            for (let i = 0; i < uniqueValues.length; i++) {
                if (rule.datatype === 'float64')
                    uniqueValues[i] = parseFloat(uniqueValues[i].trim());
                else if (rule.datatype === 'int64' || rule.datatype === 'uint8')
                    uniqueValues[i] = parseInt(uniqueValues[i].trim());
                else
                    uniqueValues[i] = String(uniqueValues[i].trim());
            }
            setRule({ ...rule, 'unique_count': uniqueValues.length, [e.target.name]: uniqueValues });
            setUniqueCount(uniqueValues.length);
        }
        else if (e.target.name === 'ordinal_order') {
            let uniqueValues = e.target.value.split(',');
            for (let i = 0; i < uniqueValues.length; i++) {
                uniqueValues[i] = parseInt(uniqueValues[i].trim());
            }
            setRule({ ...rule, [e.target.name]: uniqueValues });
        }
        else if (e.target.name === 'max' || e.target.name === 'min' || e.target.name === 'mode' || e.target.name === 'mean') {
            setRule({ ...rule, [e.target.name]: e.target.value === '' ? null : parseFloat(e.target.value) });
        }
        else {
            setRule({ ...rule, [e.target.name]: e.target.value === '' ? null : e.target.value });
        }
    }

    useImperativeHandle(props.childRef, () => ({
        collectData() {
            var temp_rule = rule;
            if (temp_rule.unique_values !== null) {
                var uniqueValues = temp_rule.unique_values;
                for (let i = 0; i < uniqueValues.length; i++) {
                    if (rule.datatype === 'float64')
                        uniqueValues[i] = parseFloat(uniqueValues[i].trim());
                    else if (rule.datatype === 'int64' || rule.datatype === 'uint8')
                        uniqueValues[i] = parseInt(uniqueValues[i].trim());
                    else
                        uniqueValues[i] = String(uniqueValues[i].trim());
                }
                temp_rule.unique_values = uniqueValues;
            }
            return temp_rule;
        }
    }));

    return (
        <div className="card card-width-fixed mx-2">
            {recommendation !== null && statistics != null ?
                <div className="card-body">
                    {/* COLUMN NAME */}
                    <div className="mb-2">
                        <label className="form-label">Column Name:</label>
                        <input type="text" className="form-control" defaultValue={recommendation.column_name} disabled />
                    </div>
                    {/* DROP COLUMN */}
                    <div className="mb-2">
                        <div className="form-check form-switch">
                            <input className="form-check-input" type="checkbox" role="switch" defaultChecked={false} onChange={toggleDropColumn} />
                            <label className="form-check-label">Drop column?</label>
                        </div>
                    </div>
                    {/* CATEGORICAL */}
                    <div className="mb-2" title={"Suggested: " + !statistics.is_numeric} data-plugin="tippy">
                        <div className="form-check form-switch">
                            <input className="form-check-input" type="checkbox" role="switch" defaultChecked={!recommendation.is_numeric} onChange={toggleNumeric} name="is_numeric" disabled={dropColumn} />
                            <label className="form-check-label">Is categorical?</label>
                        </div>
                    </div>
                    {/* COLUMN TYPE */}
                    <div className="mb-2" title={"Original: " + statistics.original_datatype} data-plugin="tippy">
                        <label className="form-label">Column Type:</label>
                        <select ref={columnType} defaultValue={recommendation.datatype} name="datatype" onChange={restructureRule} disabled={dropColumn}>
                            <option value="object">object</option>
                            <option value="int64">int64</option>
                            <option value="float64">float64</option>
                            <option value="uint8">uint8</option>
                        </select>
                    </div>
                    {/* MINIMUM VALUE */}
                    <div className="mb-2" title={statistics.min != null ? "Original: " + statistics.min : null} data-plugin="tippy">
                        <label className="form-label">Minimum Value:</label>
                        <input type="text" className="form-control" defaultValue={recommendation.min} disabled={!is_numeric || dropColumn} name="min" onChange={restructureRule} />
                    </div>
                    {/* MAXIMUM VALUE */}
                    <div className="mb-2" title={statistics.max != null ? "Original: " + statistics.max : null} data-plugin="tippy">
                        <label className="form-label">Maximum Value:</label>
                        <input type="text" className="form-control" defaultValue={recommendation.max} disabled={!is_numeric || dropColumn} name="max" onChange={restructureRule} />
                    </div>
                    {/* AVERAGE/MODE VALUE */}
                    {recommendation.is_numeric ?
                        <div className="mb-2" title={statistics.mean != null ? "Original: " + statistics.mean : null} data-plugin="tippy">
                            <label className="form-label">Mean Value:</label>
                            <input type="text" className="form-control" defaultValue={recommendation.mean} disabled name="mean" />
                        </div> :
                        <div className="mb-2" title={statistics.mode != null ? "Original: " + statistics.mode : null} data-plugin="tippy">
                            <label className="form-label">Mode Value:</label>
                            <input type="text" className="form-control" defaultValue={recommendation.mode} disabled name="mode" />
                        </div>
                    }
                    {/* UNIQUE COUNTS */}
                    <div className="mb-2" title={statistics.unique_count != null ? "Original: " + statistics.unique_count : null} data-plugin="tippy">
                        <label className="form-label">Unique Counts:</label>
                        <input type="text" className="form-control" value={uniqueCount} disabled name="unique_count" onChange={restructureRule} />
                    </div>
                    {/* UNIQUE VALUES */}
                    <div className="mb-2" title={statistics.unique_values != null ? "Original: " + statistics.unique_values.split(',').splice(0, statistics.unique_count > 30 ? 30 : statistics.unique_count).toString() : null} data-plugin="tippy">
                        <label className="form-label">Unique Values:</label>
                        <input type="text" className="form-control" defaultValue={recommendation.unique_values} disabled={is_numeric || dropColumn} name="unique_values" onChange={restructureRule} />
                    </div>
                    {/* FILL METHOD */}
                    <div className="mb-2" title={"Suggested: " + recommendation.fill_method} data-plugin="tippy">
                        <label className="form-label">Fill Method:</label>
                        <select ref={columnFill} defaultValue={recommendation.fill_method} name="fill_method">
                            <option value="">Select a fill method</option>
                            <option value="automatic">Automatic</option>
                            <option value="column">Drop Column</option>
                            <option value="row">Drop Row</option>
                            <option value="average">Average/Mode</option>
                            <option value="knn">KNN Impute</option>
                        </select>
                    </div>
                    {/* NOMINAL OR ORDINAL */}
                    <div className="mb-2" title={"Suggested: " + recommendation.is_nominal} data-plugin="tippy">
                        <div className="form-check form-switch">
                            <input className="form-check-input" type="checkbox" role="switch" defaultChecked={recommendation.is_nominal} onChange={toggleNominal} disabled={is_numeric || dropColumn} name="is_nominal" />
                            <label className="form-check-label">Is nominal?</label>
                        </div>
                    </div>
                    {/* ORDERLIST VALUES */}
                    <div className="mb-1">
                        <label className="form-label mb-0">Order Values:</label><br />
                        <small className="text-muted">CSV: 0,1,2</small>
                        <input type="text" className="form-control" placeholder="0,1,2" disabled={!(is_numeric === false && is_nominal === false) || dropColumn ? true : false} name="ordinal_order" onChange={restructureRule} />
                    </div>
                </div> : null}
        </div>
    );
}

export default ColumnRules;