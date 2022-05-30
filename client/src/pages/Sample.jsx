import React from "react";
import Navigation from "../components/structure/Navigation";
import SideBar from "../components/structure/SideBar";
import Footer from "../components/structure/Footer";

function Sample() {
    return (
        <div id='wrapper'>
            <title>Home | Lighthouse AI</title>
            <Navigation />
            <SideBar />
            <div className="content-page">
                <div className="content">
                    <div className="container-fluid scroll mt-0">
                        <h1>hi</h1>
                        <h1>hi</h1>
                        <h1>hi</h1>
                        <h1>hi</h1>
                        <h1>hi</h1>
                        <h1>hi</h1>
                        <h1>hi</h1>
                        <h1>hi</h1>
                        <h1>hi</h1>
                        <h1>hi</h1>
                        <h1>hi</h1>
                        <h1>hi</h1>
                        <h1>hi</h1>
                        <Footer />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Sample;