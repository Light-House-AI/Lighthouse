import React from "react";

import Navigation from "../components/structure/Navigation";
import Footer from "../components/structure/Footer";
import SideBar from "../components/structure/SideBar";
import PageTitle from "../components/structure/PageTitle";
import CreateModel from "../components/CreateModel";

function CreateModelPage() {
    return (
        <div id='wrapper'>
            <title>Create Model - Project 1 | Lighthouse AI</title>
            <Navigation />
            <SideBar />
            <div className="content-page">
                <div className="content">
                    <div className="container-fluid scroll">
                        <PageTitle project={"Project 1"} type={"Models"} view={"Create Model"} projectid={"asdasd"} />
                        <div className="mb-2">
                            <CreateModel />
                        </div>
                        <Footer />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default CreateModelPage;