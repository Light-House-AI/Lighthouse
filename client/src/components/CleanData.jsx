import React, { useState, useEffect } from "react";
import axios from "axios";

import ColumnRules from "./ColumnRules";

function CleanData(props) {
    const [datasetIds] = useState(props.datasetIds);
    const [recommendations, setRecommendations] = useState(null);

    useEffect(() => {

        axios.get('/datasets/raw/recommendations/', {
            params: {
                datasets_ids: datasetIds
            },
            headers: {
                'Content-Type': 'application/json',
                'Authorization': localStorage.getItem('tokenType').toString() + " " + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setRecommendations(response.data);
        }).catch((error) => {
        });
    }, []);

    return (
        <div className="row recommendation">
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
                    {recommendations !== null ?
                        recommendations.map((recommendation, index) => {
                            return (
                                <ColumnRules key={index} recommendation={recommendation} statistics={recommendation} />
                            );
                        }) : null}
                </div>
            </div>
        </div>
    );
}

export default CleanData;