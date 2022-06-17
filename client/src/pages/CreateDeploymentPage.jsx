import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import axios from "axios";

import Navigation from "../components/structure/Navigation";
import Footer from "../components/structure/Footer";
import SideBar from "../components/structure/SideBar";
import PageTitle from "../components/structure/PageTitle";

import CreateDeployment from "../components/CreateDeployment";

function CreateDeploymentPage() {
    const { projectid, modelid } = useParams();
    const [projectDetails, setProjectDetails] = useState(null);

    useEffect(() => {
        axios.get(`/projects/${projectid}/`, {
            headers: {
                "Content-Type": "application/json",
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setProjectDetails(response.data);
        });
    }, []);

    return (
        <div id='wrapper'>
            <Navigation />
            {projectDetails !== null ?
                <SideBar projectDetails={projectDetails} /> : null}
            <div className="content-page">
                {projectDetails !== null ?
                    <div className="content">
                        <title>Create Deployment - {window.capitalizeFirstLetter(projectDetails.name)} | Lighthouse AI</title>
                        <div className="container-fluid scroll">
                            <PageTitle project={window.capitalizeFirstLetter(projectDetails.name)} type={"Deployments"} view={"Create Deployment"} execution={null} projectid={projectid} />
                            <div className="mb-2">
                                <CreateDeployment projectId={projectid} modelId={modelid} />
                            </div>
                            <Footer />
                        </div>
                    </div> : null}
            </div>
        </div>
    );
}

export default CreateDeploymentPage;