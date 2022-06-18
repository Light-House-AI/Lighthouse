import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import axios from "axios";

import Navigation from "../components/structure/Navigation";
import Footer from "../components/structure/Footer";
import SideBar from "../components/structure/SideBar";
import PageTitle from "../components/structure/PageTitle";

import PredictDeployment from "../components/PredictDeployment";

function PredictPage() {
    const { projectid, deploymentid } = useParams();
    const [projectDetails, setProjectDetails] = useState(null);
    const [projectColumns, setProjectColumns] = useState(null);
    const [deploymentDetails, setDeploymentDetails] = useState(null);

    useEffect(() => {
        axios.get(`/projects/${projectid}/`, {
            headers: {
                "Content-Type": "application/json",
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setProjectDetails(response.data);
        });

        axios.get(`/projects/${projectid}/columns`, {
            headers: {
                "Content-Type": "application/json",
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setProjectColumns(response.data);
        });

        axios.get(`/deployments/${deploymentid}/`, {
            headers: {
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setDeploymentDetails(response.data);
        }).catch((error) => {
        });
    }, []);

    return (
        <div id='wrapper'>
            <Navigation />
            {projectDetails !== null ?
                <SideBar projectDetails={projectDetails} /> : null}
            <div className="content-page">
                {projectDetails !== null && deploymentDetails !== null && projectColumns !== null ?
                    <div className="content">
                        <title>Predict {window.capitalizeFirstLetter(deploymentDetails.name)} - {window.capitalizeFirstLetter(projectDetails.name)} | Lighthouse AI</title>
                        <div className="container-fluid scroll">
                            <PageTitle project={window.capitalizeFirstLetter(projectDetails.name)} type={"Deployments"} view={window.capitalizeFirstLetter(deploymentDetails.name)} execution={"Predict"} projectid={projectid} />
                            <div className="my-4">
                                <PredictDeployment projectDetails={projectDetails} deploymentDetails={deploymentDetails} columns={projectColumns} />
                            </div>
                            <Footer />
                        </div>
                    </div> : null}
            </div>
        </div>
    );
}

export default PredictPage;