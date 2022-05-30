import React, { useState } from "react";

function PageTitle(props) {
    const [project] = useState(props.project);
    const [type] = useState(props.type);
    return (
        <div className="row">
            <div className="col-12">
                <div className="page-title-box">
                    <div className="page-title-right">
                        <ol className="breadcrumb m-0">
                            <li className="breadcrumb-item">Lighthouse</li>
                            <li className="breadcrumb-item">{project}</li>
                            <li className="breadcrumb-item active">{type}</li>
                        </ol>
                    </div>
                    <h4 className="page-title">{type}</h4>
                </div>
            </div>
        </div>
    );
}

export default PageTitle;