import React, { useState } from "react";

function PageTitle(props) {
    const [project] = useState(props.project);
    const [type] = useState(props.type);
    const [view] = useState(props.view);
    const [projectid] = useState(props.projectid);
    return (
        <div className="row">
            <div className="col-12">
                <div className="page-title-box">
                    <div className="page-title-right">
                        <ol className="breadcrumb m-0">
                            <li className="breadcrumb-item"><a href="/">Lighthouse</a></li>
                            <li className="breadcrumb-item"><a href={"/" + projectid}>{project}</a></li>
                            {view === null ?
                                <li className="breadcrumb-item active">{type}</li> :
                                <li className="breadcrumb-item"><a href={"/" + projectid + "/" + type.toLowerCase()}>{type}</a></li>
                            }
                            {view !== null ?
                                <li className="breadcrumb-item active">{view}</li> : null}
                        </ol>
                    </div>
                    {view === null ?
                        <h4 className="page-title">{type}</h4> :
                        <h4 className="page-title">{view}</h4>
                    }
                </div>
            </div>
        </div>
    );
}

export default PageTitle;