import React, { useState } from "react";

function GenericModal(props) {
    const [hideNext] = useState(props.hideNext);

    return (
        <div id="modal-structure">
            <button id="modal-trigger" type="button" className="btn btn-primary d-none" data-bs-toggle="modal" data-bs-target="#generic-modal">Open first modal</button>
            <div id="generic-modal" className="modal fade" tabIndex="-1">
                <div className="modal-dialog modal-dialog-centered">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 id="modal-title" className="modal-title"> </h5>
                        </div>
                        <div id="modal-body" className="modal-body bg-light">
                        </div>
                        <div id="modal-footer" className="modal-footer">
                            <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button id='modal-btn' type="button" className={hideNext ? "btn btn-primary d-none" : "btn btn-primary"}><i className="fe-arrow-right me-1"></i>Next</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default GenericModal;