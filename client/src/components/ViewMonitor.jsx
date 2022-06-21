import React, { useState, useEffect } from "react";
import axios from "axios";

function ViewMonitor(props) {
    const [deploymentDetails] = useState(props.deploymentDetails);
    useEffect(() => {
        axios.get(`/deployments/${deploymentDetails.id}/monitoring`, {
            headers: {
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken'),
                'Access-Control-Allow-Origin': '*',
            }
        }).then((response) => {
            // debugger;
            document.getElementById('monitor').srcdoc = response.data;
            window.iframeId = window.setInterval(() => {
                let iframeTag = document.getElementById('monitor');
                let iframeDoc = iframeTag.contentDocument || iframeTag.contentWindow.document;

                if (iframeDoc.readyState === 'complete') {
                    window.$('#monitor').contents().find('body').find('nav').remove();
                    window.$('#monitor').contents().find('body').find('.col-lg-2').remove();
                    window.$('#monitor').contents().find('body').find('#section-1-content-block-3').remove();
                    window.$('#monitor').contents().find('body').find('#section-1-content-block-1-subheader').remove();
                    window.$('#monitor').contents().find('body').find('.container-fluid .row .col-md-10').removeClass().addClass('col-12')
                    window.$('#monitor').contents().find('body').find('.search-input').remove();
                    window.$("#monitor").contents().find("head").append("<style>*{color: #fff !important;} body {background-color: #303841;} .alert-secondary { background-color: #37424c !important; border-color: #37424c !important; } ::-webkit-scrollbar { width: 5px; height: 5px; } ::-webkit-scrollbar-track { background-color: rgba(0, 0, 0, 0.0); } ::-webkit-scrollbar-thumb { background-color: #888; border-radius: 10px; cursor: pointer; }</style>");
                    window.$('#deployment-monitor').removeClass('invisible');
                    window.clearInterval(window.iframeId);
                }
            }, 500);
        }).catch((error) => {
        });
    }, []);

    return (
        <div>
            <div id="deployment-monitor" className="invisible">
                <iframe id="monitor" title="test" className="w-100 iframe-height"></iframe>
            </div>
        </div>
    );
}

export default ViewMonitor;