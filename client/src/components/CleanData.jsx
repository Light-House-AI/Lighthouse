import React, { useState, useEffect } from "react";
import axios from "axios";

import ColumnRules from "./ColumnRules";

function CleanData(props) {
    const [datasetIds] = useState(props.datasetIds);
    const [projectId] = useState(props.projectid);
    const [recommendations, setRecommendations] = useState(null);
    const [columnsRef, setColumnsRef] = useState(null);

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
            let refs = [];
            for (let i = 0; i < response.data.length; i++) {
                refs.push(React.createRef());
            }
            setColumnsRef(refs);
        }).catch((error) => {
        });
    }, []);

    useEffect(() => {
        window.activateHorizontalScroll();
    }, [recommendations]);

    const updateRules = function () {
        document.getElementById('error-div').classList.add('d-none');

        document.getElementById('next-btn').classList.add('disabled');
        window.$("#loading-btn").html('<div class="spinner-border spinner-border-sm text-white me-1" role="status"></div>');

        if (document.getElementById('dataset-name').value === '') {
            document.getElementById('error-msg').innerHTML = 'Please enter a name for the dataset';
            document.getElementById('error-div').classList.remove('d-none');

            document.getElementById('next-btn').classList.remove('disabled');
            window.$("#loading-btn").html('<i class="fe-check-circle me-1"></i>');
            return;
        }

        let all_rules = [];
        for (let i = 0; i < columnsRef.length; i++) {
            let rule = columnsRef[i].current.collectData();
            all_rules.push(rule);
        }

        const data = {
            project_id: parseInt(projectId),
            name: document.getElementById('dataset-name').value,
            sources: datasetIds.map(id => parseInt(id)),
            rules: all_rules
        };
        axios.post('/datasets/cleaned/', data, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': localStorage.getItem('tokenType') + " " + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            window.location.href = `/${projectId}/models/${response.data.id}/create`;
        }).catch((error) => {
            document.getElementById('next-btn').classList.remove('disabled');
            window.$("#loading-btn").html('<i class="fe-check-circle me-1"></i>');
        });
    }

    return (
        <div className="row recommendation">
            <div className="col-12 mb-2">
                <div className="row">
                    <div className="col-9">
                        <div className="row h-100 align-items-center">
                            <div className="col-md-3 col-4 d-flex align-items-center">
                                <p className="form-label m-0">New Dataset Name:</p>
                            </div>
                            <div className="col-md-4 col-4">
                                <input type="text" className="form-control" id="dataset-name" />
                            </div>
                            <div id='error-div' className="col-md-5 col-4 d-none">
                                <label id="error-msg" className="text-danger"></label>
                            </div>
                        </div>
                    </div>
                    <div className="col-3 text-center d-flex justify-content-end">
                        <button type="button" className="btn btn-light waves-effect waves-light m-1"><i className="fe-x me-1"></i>Cancel</button>
                        <button id="next-btn" type="button" className="btn btn-success waves-effect waves-light m-1" onClick={updateRules}>
                            <div id="loading-btn" className="d-inline">
                                <i className="fe-check-circle me-1"></i>
                            </div>
                            Create
                        </button>
                    </div>
                </div>
            </div>
            <div className="col-12">
                <div className="row overflow-x-scroll enable-row-overflow-x me-1">
                    {recommendations !== null ?
                        recommendations.map((recommendation, index) => {
                            recommendation.unique_values = recommendation.unique_values !== null ? recommendation.unique_values.toString() : '';
                            return (
                                <ColumnRules childRef={columnsRef[index]} key={`col-${index}`} recommendation={recommendation} statistics={recommendation} />
                            );
                        }) : null}
                </div>
            </div>
        </div>
    );
}

export default CleanData;