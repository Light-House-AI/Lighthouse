import React, { useState } from "react";
import { useParams } from 'react-router-dom';

function SideBar(props) {
    const { projectid } = useParams();
    const [userDetails] = useState(JSON.parse(localStorage.getItem("user")));
    const [projectDetails] = useState(props.projectDetails);

    const logOut = function () {
        localStorage.clear();
        window.location.href = "/login";
    }
    return (
        <div className="left-side-menu">
            <div className="h-100 scroll-bar">
                <div className="user-box text-center">
                    <img src="/user.jpg" alt="user-img" title="Mat Helme"
                        className="rounded-circle avatar-md" />
                    <div className="dropdown">
                        <a href="/" className="text-dark dropdown-toggle h5 mt-2 mb-1 d-block"
                            data-bs-toggle="dropdown">{window.capitalizeFirstLetter(userDetails.first_name)} {window.capitalizeFirstLetter(userDetails.last_name)}</a>
                        <div className="dropdown-menu user-pro-dropdown">
                            <button className="dropdown-item notify-item" onClick={logOut}>
                                <i className="fe-log-out me-1"></i>
                                <span>Logout</span>
                            </button>
                        </div>
                    </div>
                    <p className="text-muted">{window.capitalizeFirstLetter(userDetails.role)}</p>
                </div>
                <div id="sidebar-menu">
                    <ul id="side-menu">
                        {/* DATASETS */}
                        <li>
                            <a href="#datasets" data-bs-toggle="collapse">
                                <i className="fe-file-text"></i>
                                <span className="badge bg-success rounded-pill float-end">{projectDetails.raw_datasets.length + projectDetails.cleaned_datasets.length}</span>
                                <span> Datasets </span>
                            </a>
                            <div className="collapse" id="datasets">
                                <ul className="nav-second-level">
                                    <li>
                                        <a href={`/${projectid}/datasets`}>All Datasets</a>
                                    </li>
                                    <li>
                                        <a href="#rawdata" data-bs-toggle="collapse">
                                            <span className="badge bg-success rounded-pill">{projectDetails.raw_datasets.length}</span> Raw Datasets <span className="menu-arrow"></span>
                                        </a>
                                        <div className="collapse" id="rawdata">
                                            <ul className="nav-second-level">
                                                {projectDetails.raw_datasets.map((record, index) => {
                                                    return (
                                                        <li key={index}>
                                                            {/* `/${record.project_id}/datasets/raw/${record.id}/view` */}
                                                            <a href={`/${record.project_id}/datasets/raw/${record.id}/view`}>{record.name}</a>
                                                        </li>
                                                    );
                                                })}
                                            </ul>
                                        </div>
                                    </li>
                                    <li>
                                        <a href="#cleaneddatasets" data-bs-toggle="collapse">
                                            <span className="badge bg-success rounded-pill">{projectDetails.cleaned_datasets.length}</span> Cleaned Datasets <span className="menu-arrow"></span>
                                        </a>
                                        <div className="collapse" id="cleaneddatasets">
                                            <ul className="nav-second-level">
                                                {projectDetails.cleaned_datasets.map((record, index) => {
                                                    return (
                                                        <li key={index}>
                                                            {/* `/${record.project_id}/datasets/cleaned/${record.id}/view` */}
                                                            <a href={`/${record.project_id}/datasets/cleaned/${record.id}/view`}>{record.name}</a>
                                                        </li>
                                                    );
                                                })}
                                            </ul>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </li>

                        {/* MODELS */}
                        <li>
                            <a href="#models" data-bs-toggle="collapse">
                                <i className="fe-box"></i>
                                <span className="badge bg-success rounded-pill float-end">{projectDetails.models.length}</span>
                                <span> Models </span>
                            </a>
                            <div className="collapse" id="models">
                                <ul className="nav-second-level">
                                    <li>
                                        <a href={`/${projectid}/models`}>All Models</a>
                                    </li>
                                    {projectDetails.models.map((record, index) => {
                                        return (
                                            <li key={index}>
                                                {/* `/${record.project_id}/models/${record.id}/view` */}
                                                <a href={`/${record.project_id}/models/${record.id}/view`}>{record.name}</a>
                                            </li>
                                        );
                                    })}
                                </ul>
                            </div>
                        </li>

                        {/* DEPLOYMENTS */}
                        <li>
                            <a href="#deployments" data-bs-toggle="collapse">
                                <i className="fe-cloud-lightning"></i>
                                <span className="badge bg-success rounded-pill float-end">{projectDetails.deployments.length}</span>
                                <span> Deployments </span>
                            </a>
                            <div className="collapse" id="deployments">
                                <ul className="nav-second-level">
                                    <li>
                                        <a href={`/${projectid}/deployments`}>All Deployments</a>
                                    </li>
                                    {projectDetails.deployments.map((record, index) => {
                                        return (
                                            <li key={index}>
                                                {/* `/${record.project_id}/deployments/${record.id}/view` */}
                                                <a href={`/${record.project_id}/deployments/${record.id}/view`}>{record.name}</a>
                                            </li>
                                        );
                                    })}
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