import React, { useEffect } from "react";

import Navigation from "../components/structure/Navigation";
import Footer from "../components/structure/Footer";
import Project from "../components/Project";

function HomePage() {
    useEffect(() => {
        document.getElementsByTagName("body")[0].classList.add("overflow-y-scroll");
    }, []);

    if (localStorage.getItem('accessToken') === null) {
        window.location.href = '/login';
    }

    return (
        <div id="wrapper">
            <title>Home | Lighthouse AI</title>
            <Navigation />
            <div className="homepage container-fluid mb-3">
                <div className="row mx-2">
                    <div className="col-xl-4 col-md-6">
                        <Project data={{ name: 'Project 1', datasets: 3, models: 3, deployments: 3 }} _id={1} />
                    </div>
                    <div className="col-xl-4 col-md-6">
                        <Project data={{ name: 'Project 2', datasets: 3, models: 3, deployments: 3 }} _id={2} />
                    </div>
                    <div className="col-xl-4 col-md-6">
                        <Project data={{ name: 'Project 2', datasets: 3, models: 3, deployments: 3 }} _id={3} />
                    </div>
                    <div className="col-12">
                        <Footer />
                    </div>
                </div>
            </div>

        </div >
    );
}

export default HomePage;