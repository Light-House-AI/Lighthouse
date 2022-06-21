import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import axios from "axios";

import Navigation from "../components/structure/Navigation";
import SideBar from "../components/structure/SideBar";
import Footer from "../components/structure/Footer";
import PageTitle from "../components/structure/PageTitle";

import ApexChart from "../components/ApexChart";

function DataVisualizationPage() {
    const { projectid } = useParams();
    const { datasetid } = useParams();
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
            {projectDetails !== null ?
                <div className="content-page">
                    <title>Visualize ABC - {projectDetails.name} | Lighthouse AI</title>
                    <div className="content">
                        <div className="container-fluid scroll">
                            <PageTitle project={window.capitalizeFirstLetter(projectDetails.name)} type={"Datasets"} view={"ABC"} execution={"Visaulize"} projectid={projectid} />
                            <div className="mb-2">
                                <ApexChart plotType={`Line Chart`} columns={['Age', 'Fare']} />
                            </div>
                            <Footer />
                        </div>
                    </div>
                </div> : null}
        </div>
    );
}

export default DataVisualizationPage;