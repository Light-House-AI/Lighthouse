import React from "react";

import Navigation from "../components/structure/Navigation";
import Project from "../components/Project";

function Homepage() {
    return (
        <div id="wrapper">
            <title>Home | Lighthouse AI</title>
            <Navigation />
            <div className="homepage container-fluid">
                <div className="row overflow-y-scroll mx-2">
                    <div className="col-xl-4 col-md-6">
                        <Project data={{ name: 'Project 1', datasets: 3, models: 3, deployments: 3 }} _id={1} />
                    </div>
                    <div className="col-xl-4 col-md-6">
                        <Project data={{ name: 'Project 2', datasets: 3, models: 3, deployments: 3 }} _id={2} />
                    </div>
                    <div className="col-xl-4 col-md-6">
                        <Project data={{ name: 'Project 2', datasets: 3, models: 3, deployments: 3 }} _id={3} />
                    </div>
                </div>
            </div>
        </div >
    );
}

export default Homepage;