import React from "react";

function SideBar() {
    return (
        <div className="left-side-menu">
            <div className="h-100 scroll-bar">
                <div className="user-box text-center">
                    <img src="/user.jpg" alt="user-img" title="Mat Helme"
                        className="rounded-circle avatar-md" />
                    <div className="dropdown">
                        <a href="/" className="text-dark dropdown-toggle h5 mt-2 mb-1 d-block"
                            data-bs-toggle="dropdown">Stanley Parker</a>
                        <div className="dropdown-menu user-pro-dropdown">
                            <a href="/" className="dropdown-item notify-item">
                                <i className="fe-log-out me-1"></i>
                                <span>Logout</span>
                            </a>
                        </div>
                    </div>
                    <p className="text-muted">Admin Head</p>
                </div>
                <div id="sidebar-menu">
                    <ul id="side-menu">
                        {/* DATASETS */}
                        <li>
                            <a href="#datasets" data-bs-toggle="collapse">
                                <i className="fe-file-text"></i>
                                <span className="badge bg-success rounded-pill float-end">4</span>
                                <span> Datasets </span>
                            </a>
                            <div className="collapse" id="datasets">
                                <ul className="nav-second-level">
                                    <li>
                                        <a href="/">Dataset 1</a>
                                    </li>
                                    <li>
                                        <a href="/">Dataset 2</a>
                                    </li>
                                    <li>
                                        <a href="/">Dataset 3</a>
                                    </li>
                                    <li>
                                        <a href="/">Dataset 4</a>
                                    </li>
                                </ul>
                            </div>
                        </li>

                        {/* MODELS */}
                        <li>
                            <a href="#models" data-bs-toggle="collapse">
                                <i className="fe-box"></i>
                                <span className="badge bg-success rounded-pill float-end">4</span>
                                <span> Models </span>
                            </a>
                            <div className="collapse" id="models">
                                <ul className="nav-second-level">
                                    <li>
                                        <a href="/">Model 1</a>
                                    </li>
                                    <li>
                                        <a href="/">Model 2</a>
                                    </li>
                                    <li>
                                        <a href="/">Model 3</a>
                                    </li>
                                    <li>
                                        <a href="/">Model 4</a>
                                    </li>
                                </ul>
                            </div>
                        </li>

                        {/* DEPLOYMENTS */}
                        <li>
                            <a href="#deployments" data-bs-toggle="collapse">
                                <i className="fe-cloud-lightning"></i>
                                <span className="badge bg-success rounded-pill float-end">4</span>
                                <span> Deployments </span>
                            </a>
                            <div className="collapse" id="deployments">
                                <ul className="nav-second-level">
                                    <li>
                                        <a href="/">Deployment 1</a>
                                    </li>
                                    <li>
                                        <a href="/">Deployment 2</a>
                                    </li>
                                    <li>
                                        <a href="/">Deployment 3</a>
                                    </li>
                                    <li>
                                        <a href="/">Deployment 4</a>
                                    </li>
                                </ul>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default SideBar;