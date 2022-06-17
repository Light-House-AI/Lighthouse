import axios from "axios";
import React, { useEffect, useRef, useState } from "react";

function ViewDataset(props) {
    const tableRef = useRef(null);
    const [datasetId] = useState(props.datasetId);
    const [datasetType] = useState(props.datasetType);
    useEffect(() => {
        axios.get(`/datasets/${datasetType}/${datasetId}/rows?limit=1`, {
            headers: {
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            let columnNames = Object.keys(response.data[0]);
            let dtColumns = [];
            for (let i = 0; i < columnNames.length; i++) {
                dtColumns.push({
                    title: columnNames[i],
                    data: columnNames[i]
                });
            }
            if (!(window.dt === undefined || window.dt === null)) {
                window.dt = window.dt.destroy();
            }
            window.dt = window.$(tableRef.current).DataTable({
                searching: false,
                ordering: false,
                scrollCollapse: true,
                scrollY: "45vh",
                scrollX: true,
                columns: dtColumns,
                bInfo: false,
                serverSide: true,
                processing: true,
                ajax: {
                    type: "GET",
                    url: `${window.baseURL}/datasets/${datasetType}/${datasetId}/rows/`,
                    headers: {
                        'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
                    },
                    data: function (d) {
                        localStorage.setItem('draw', d.draw);
                        const dataSend = {
                            skip: d.start,
                            limit: d.length,
                        }
                        return dataSend
                    },
                    dataSrc: ""
                }
            });
        });
    }, []);
    return (
        <div className="table-responsive view-dataset">
            <table ref={tableRef} className="table nowrap w-100 no-footer">
                <thead>
                </thead>
            </table>
        </div>
    );
}

export default ViewDataset;