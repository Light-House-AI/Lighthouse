import React, { useState, useEffect } from "react";

import { Morris } from 'morris.js06';

function Project(props) {
    const [project] = useState(props.data);
    const [_id] = useState(props._id);
    console.log('twice')

    useEffect(() => {
        console.log("test")
        if (project !== null) {
            document.getElementById(`project-${_id}`).innerHTML = "";
            Morris.Donut({
                element: 'project-' + _id,
                data: [
                    { label: "Datasets", value: project.datasets === null ? 0 : project.datasets },
                    { label: "Models", value: project.models === null ? 0 : project.models },
                    { label: "Deployments", value: project.deployments === null ? 0 : project.deployments }
                ],
                barSize: 0.2,
                resize: true,
                colors: ['#4fc6e1', '#6658dd', '#ebeff2'],
                backgroundColor: 'transparent'
            });
        }
    }, []);

    return (
        <div className="card">
            {project !== null ?
                <div className="card-body">
                    <div className="card-widgets">
                        <a data-bs-toggle="collapse" href={"#cardCollpase" + _id} role="button" aria-expanded="false" aria-controls="cardCollpase1">
                            <i className="mdi mdi-minus"></i>
                        </a>
                    </div>
                    <a className="text-muted header-title mb-0 cursor-pointer cursor-pointer fs-4" href={"/" + project.id}>{window.capitalizeFirstLetter(project.name)}</a>

                    <div id={"cardCollpase" + _id} className="collapse pt-3 show">
                        <div className="text-center">
                            <div className="row mt-2">
                                <div className="col-4">
                                    <h3 data-plugin="counterup">{project.datasets === null ? 0 : project.datasets}</h3>
                                    <p className="text-muted font-13 mb-0 text-truncate">Datasets</p>
                                </div>
                                <div className="col-4">
                                    <h3 data-plugin="counterup">{project.models === null ? 0 : project.models}</h3>
                                    <p className="text-muted font-13 mb-0 text-truncate">Models</p>
                                </div>
                                <div className="col-4">
                                    <h3 data-plugin="counterup">{project.deployments === null ? 0 : project.deployments}</h3>
                                    <p className="text-muted font-13 mb-0 text-truncate">Deployments</p>
                                </div>
                            </div>

                            <div dir="ltr">
                                <div id={"project-" + _id} style={{ height: "270px" }} className="morris-chart mt-3"></div>
                            </div>
                        </div>
                    </div>
                </div> : null}
        </div>
    );
}

export default Project;