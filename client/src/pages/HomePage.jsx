import React, { useEffect, useState } from "react";
import axios from 'axios';

import Navigation from "../components/structure/Navigation";
import Footer from "../components/structure/Footer";
import Project from "../components/Project";

function HomePage() {
    const [projects, setProjects] = useState([]);

    useEffect(() => {
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
                    {projects != null && projects.length > 0 ? projects.map((project) => {
                        return (
                            <div className="col-xl-4 col-md-6" key={project.id}>
                                <Project data={project} _id={1} />
                            </div>
                        );
                    }) :
                        <div className="col-12 d-flex justify-content-center align-items-center no-projects">
                            <div className="text-center">
                                <h2>No project found.</h2>
                                <a href="/newproject">Create new project?</a>
                            </div>
                        </div>
                    }
                    <div className="col-12">
                        <Footer />
                    </div>
                </div>
            </div>

        </div >
    );
}

export default HomePage;