import React, { useState, useEffect } from "react";
import axios from "axios";

import ViewRules from "./ViewRules";

function RuleData(props) {
    const [datasetId] = useState(props.datasetId);
    const [projectId] = useState(props.projectid);
    const [rules, setRules] = useState(null);

    useEffect(() => {

        axios.get(`/datasets/cleaned/${datasetId}/cleaning_rules/`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': localStorage.getItem('tokenType').toString() + " " + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setRules(response.data);
        }).catch((error) => {
        });
    }, []);

    useEffect(() => {
        window.activateHorizontalScroll();
    }, [rules]);

    return (
        <div className="row recommendation">
            <div className="col-12">
                <div className="row overflow-x-scroll enable-row-overflow-x me-1">
                    {/* {rules !== null ?
                        rules.map((rule, index) => {
                            rule.unique_values = rule.unique_values !== null ? rule.unique_values.toString() : '';
                            return (
                                <ViewRules key={`col-${index}`} rules={rule} />
                            );
                        }) : null} */}
                </div>
            </div>
        </div>
    );
}

export default RuleData;