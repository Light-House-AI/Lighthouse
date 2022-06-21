import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import axios from "axios";

import Navigation from "../components/structure/Navigation";
import Footer from "../components/structure/Footer";
import SideBar from "../components/structure/SideBar";
import PageTitle from "../components/structure/PageTitle";
import ViewModel from "../components/ViewModel.jsx";

function ViewModelPage() {
    const { projectid, modelid } = useParams();
    const [projectDetails, setProjectDetails] = useState(null);
    const [modelDetails, setModelDetails] = useState(null);

    useEffect(() => {
        axios.get(`/projects/${projectid}/`, {
            headers: {
                "Content-Type": "application/json",
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setProjectDetails(response.data);
        });

        axios.get(`/models/${modelid}`, {
            headers: {
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setModelDetails(response.data);
        })
    }, []);

    return (
        <div id='wrapper'>
            <Navigation />
            {projectDetails !== null ?
                <SideBar projectDetails={projectDetails} /> : null}
            <div className="content-page">
                {projectDetails !== null && modelDetails !== null ?
                    <div className="content">
                        <title>View {window.capitalizeFirstLetter(modelDetails.name)} - {window.capitalizeFirstLetter(projectDetails.name)} | Lighthouse AI</title>
                        <div className="container-fluid scroll">
                            <PageTitle project={window.capitalizeFirstLetter(projectDetails.name)} type={"Models"} view={window.capitalizeFirstLetter(modelDetails.name)} execution={"View"} projectid={projectid} />
                            <div className="mb-2">
                                <ViewModel modelDetails={modelDetails} type={projectDetails.type} />
                            </div>
                            <Footer />
                        </div>
                    </div> : null}
            </div>
        </div>
    );
}

export default ViewModelPage;