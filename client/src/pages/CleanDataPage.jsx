import React from "react";
import { useParams } from 'react-router-dom';

import Navigation from "../components/structure/Navigation";
import SideBar from "../components/structure/SideBar";
import Footer from "../components/structure/Footer";
import PageTitle from "../components/structure/PageTitle";

import CleanData from "../components/CleanData";

function CleanDataPage() {
    const { datasetsid } = useParams();
    return (
        <div id='wrapper'>
            <title>Create Model - Project 1 | Lighthouse AI</title>
            <Navigation />
            <SideBar />
            <div className="content-page">
                <div className="content">
                    <div className="container-fluid scroll">
                        <PageTitle project={"Project 1"} type={"Datasets"} view={"Dataset 1"} execution={"Clean"} projectid={"asdasd"} />
                        <div className="mb-2">
                            <CleanData datasetIds={datasetsid.split('-')} />
                        </div>
                        <Footer />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default CleanDataPage;