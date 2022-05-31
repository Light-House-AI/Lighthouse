import React from "react";

import Navigation from "../components/structure/Navigation";
import Footer from "../components/structure/Footer";
import SideBar from "../components/structure/SideBar";
import PageTitle from "../components/structure/PageTitle";

import CreateDeployment from "../components/CreateDeployment";

function CreateDeploymentPage() {
    return (
        <div id='wrapper'>
            <title>Create Deployment - Project 1 | Lighthouse AI</title>
            <Navigation />
            <SideBar />
            <div className="content-page">
                <div className="content">
                    <div className="container-fluid scroll">
                        <PageTitle project={"Project 1"} type={"Deployments"} view={"Create Deployment"} projectid={"asdasd"} />
                        <div className="mb-2">
                            <CreateDeployment />
                        </div>
                        <Footer />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default CreateDeploymentPage;