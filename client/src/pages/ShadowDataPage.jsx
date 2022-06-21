import React, { useEffect, useState } from "react";
import { useParams } from 'react-router-dom';
import axios from "axios";

import Navigation from "../components/structure/Navigation";
import SideBar from "../components/structure/SideBar";
import Footer from "../components/structure/Footer";
import PageTitle from "../components/structure/PageTitle";

import ShadowData from "../components/ShadowData";

function ShadowDataPage() {
    const { projectid } = useParams();
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
                        <title>Shadow Data - {window.capitalizeFirstLetter(projectDetails.name)} | Lighthouse AI</title>
                        <div className="container-fluid scroll position-relative">
                            <PageTitle project={window.capitalizeFirstLetter(projectDetails.name)} type={"Datasets"} view={"Shadow Data"} execution={"View"} projectid={projectid} />
                            <div className="mb-2">
                                <ShadowData projectId={projectid} column={projectDetails.predicted_column} />
                            </div>
                            <Footer positionBottom={true} />
                        </div>
                    </div> : null}
            </div>
        </div>
    );
}

export default ShadowDataPage;