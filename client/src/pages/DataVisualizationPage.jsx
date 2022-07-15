import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import axios from "axios";

import Navigation from "../components/structure/Navigation";
import SideBar from "../components/structure/SideBar";
import Footer from "../components/structure/Footer";
import PageTitle from "../components/structure/PageTitle";

import ApexChart from "../components/ApexChart";
import BoxPlot from "../components/BoxPlot";
import HeatMap from "../components/HeatMap";

function DataVisualizationPage() {
    const { projectid } = useParams();
    const { datasetid } = useParams();
    const { type } = useParams();
    const [columnName1] = useState(localStorage.getItem('col1'));
    const [columnName2] = useState(localStorage.getItem('col2'));

    const [projectDetails, setProjectDetails] = useState(null);
    const [datasetDetails, setDatasetDetails] = useState(null);
    const [visualization, setVisualization] = useState(null);

    useEffect(() => {
        axios.get(`/projects/${projectid}`, {
            headers: {
                "Content-Type": "application/json",
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setProjectDetails(response.data);
        });

        axios.get(`/raw_datasets/${datasetid}`, {
            headers: {
                "Content-Type": "application/json",
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            setDatasetDetails(response.data);
        });

        let columnsData = [columnName1];

        if (columnName2 !== undefined && columnName2 !== null && columnName2 !== '') {
            columnsData.push(columnName2);
        }

        if (type !== 'heatmap') {
            axios.get(`/raw_datasets/${datasetid}/visualizations`, {
                params: {
                    columns: columnsData
                },
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
                }
            }).then((response) => {
                setVisualization(response.data);
            })
        } else {
            axios.get(`/raw_datasets/${datasetid}/correlation`, {
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
                }
            }).then((response) => {
                setVisualization(response.data);
            })
        }

    }, []);

    return (
        <div id='wrapper'>
            <Navigation />
            {projectDetails !== null ?
                <SideBar projectDetails={projectDetails} /> : null}
            {projectDetails !== null && datasetDetails !== null ?
                <div className="content-page">
                    <title>Visualize {window.capitalizeFirstLetter(datasetDetails.name)} - {window.capitalizeFirstLetter(projectDetails.name)} | Lighthouse AI</title>
                    <div className="content">
                        <div className="container-fluid scroll">
                            <PageTitle project={window.capitalizeFirstLetter(projectDetails.name)} type={"Datasets"} view={window.capitalizeFirstLetter(datasetDetails.name)} execution={"Visualize"} projectid={projectid} />
                            <div className="mb-2">
                                {visualization !== null && type !== 'boxPlot' && type !== 'heatmap' ?
                                    <ApexChart plotType={type} columns={columnName2 !== undefined && columnName2 !== null && columnName2 !== '' ? [columnName1, columnName2] : [columnName1]} visualizationDetails={visualization} /> : null}
                                {visualization !== null && type === 'boxPlot' ?
                                    <BoxPlot plotType={type} columns={[columnName1]} visualizationDetails={visualization} /> : null}
                                {visualization !== null && type === 'heatmap' ?
                                    <HeatMap plotType={type} visualizationDetails={visualization} /> : null}
                            </div>
                            <Footer />
                        </div>
                    </div>
                </div> : null}
        </div>
    );
}

export default DataVisualizationPage;