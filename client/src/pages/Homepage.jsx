import React from "react";

import Navigation from "../components/structure/Navigation";
import SideBar from "../components/structure/SideBar";

function Homepage() {
    return (
        <div id='homepage'>
            <title>Home | Lighthouse AI</title>
            <Navigation />
            <SideBar />
        </div>
    );
}

export default Homepage;