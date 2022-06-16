import React from "react";

import Navigation from "../components/structure/Navigation";
import SideBar from "../components/structure/SideBar";
import Footer from "../components/structure/Footer";
import PageTitle from "../components/structure/PageTitle";
import Models from "../components/Models";

function ModelsPage() {
    return (
        <div id='wrapper'>
            <title>Models - Project 1 | Lighthouse AI</title>
            <Navigation />
            <SideBar />
            <div className="content-page">
                <div className="content">
                    <div className="container-fluid scroll">
                        <PageTitle project={"Project 1"} type={"Models"} view={null} execution={null} projectid={"asdasd"} />
                        <div className="mb-2">
                            <Models />
                        </div>
                        <Footer />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ModelsPage;