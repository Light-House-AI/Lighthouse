import React, { useEffect } from "react";

import Navigation from "../components/structure/Navigation";
import Footer from "../components/structure/Footer";
import CreateProject from "../components/CreateProject";

function CreateProjectPage() {
    useEffect(() => {
        document.getElementsByTagName("body")[0].classList.add("overflow-y-scroll");
    }, []);

    return (
        <div id="wrapper">
            <title>New Project | Lighthouse AI</title>
            <Navigation />
            <div className="homepage container-fluid mb-3">
                <div className="row mx-2">
                    <div className="col-12">
                        <CreateProject />
                    </div>
                    <div className="col-12">
                        <Footer />
                    </div>
                </div>
            </div>

        </div >
    );
}

export default CreateProjectPage;