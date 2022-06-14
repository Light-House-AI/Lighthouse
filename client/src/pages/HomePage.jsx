import React, { useEffect, useState } from "react";
import axios from 'axios';

import Navigation from "../components/structure/Navigation";
import Footer from "../components/structure/Footer";
import Project from "../components/Project";

function HomePage() {
    const [projects, setProjects] = useState([]);
    useEffect(() => {
        axios.defaults.baseURL = "http://localhost:8000/api/v1";
        document.getElementsByTagName("body")[0].classList.add("overflow-y-scroll");
        axios.get('/projects', {
            headers: { 'Authorization': localStorage.getItem('tokenType').toString() + " " + localStorage.getItem('accessToken') }
        }).then((response) => {
            setProjects(response.data);
        });
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
                    {projects !== null ? projects.map((project) => {
                        return (
                            <div className="col-xl-4 col-md-6" key={project.id}>
                                <Project data={project} _id={1} />
                            </div>
                        );
                    }) : null}

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