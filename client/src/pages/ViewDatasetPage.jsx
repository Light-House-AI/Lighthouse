import React from "react";

import Navigation from "../components/structure/Navigation";
import SideBar from "../components/structure/SideBar";
import Footer from "../components/structure/Footer";
import PageTitle from "../components/structure/PageTitle";

import ViewDataset from "../components/ViewDataset";

function ViewDatasetPage() {
    return (
        <div id='wrapper'>
            <title>Datasets - Project 1 | Lighthouse AI</title>
            <Navigation />
            <SideBar />
            <div className="content-page">
                <div className="content">
                    <div className="container-fluid scroll">
                        <PageTitle project={"Project 1"} type={"Datasets"} view={"Dataset 1"} execution={"View"} projectid={"asdasd"} />
                        <div className="mb-2">
                            <ViewDataset />
                        </div>
                        <Footer />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ViewDatasetPage;