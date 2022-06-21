import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import axios from "axios";

import Navigation from "../components/structure/Navigation";
import SideBar from "../components/structure/SideBar";
import Footer from "../components/structure/Footer";
import PageTitle from "../components/structure/PageTitle";

import RuleData from "../components/RuleData";

function RulesDataPage() {
    const { projectid } = useParams();
    const { datasetid } = useParams();
    const [projectDetails, setProjectDetails] = useState(null);
    const [datasetDetails, setDatasetDetails] = useState(null);

    useEffect(() => {
        axios.get(`/projects/${projectid}/`, {
            headers: {
                "Content-Type": "application/json",
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setProjectDetails(response.data);
        });

        axios.get(`/datasets/cleaned/${datasetid}/`, {
            headers: {
                "Content-Type": "application/json",
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setDatasetDetails(response.data);
        });
    }, []);

    return (
        <div id='wrapper'>
            <Navigation />
            {projectDetails !== null ?
                <SideBar projectDetails={projectDetails} /> : null}
            {projectDetails !== null && datasetDetails !== null ?
                <div className="content-page">
                    <title>View Rules {window.capitalizeFirstLetter(datasetDetails.name)} - {window.capitalizeFirstLetter(projectDetails.name)} | Lighthouse AI</title>
                    <div className="content">
                        <div className="container-fluid scroll">
                            <PageTitle project={window.capitalizeFirstLetter(projectDetails.name)} type={"Datasets"} view={window.capitalizeFirstLetter(datasetDetails.name)} execution={"View Rules"} projectid={projectid} />
                            <div className="mb-2">
                                <RuleData datasetId={datasetid} projectid={projectid} />
                            </div>
                            <Footer />
                        </div>
                    </div>
                </div> : null}
        </div>
    );
}

export default RulesDataPage;