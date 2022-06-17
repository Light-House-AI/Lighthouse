import axios from "axios";
import React, { useEffect, useRef, useState } from "react";

function ViewDataset(props) {
    const tableRef = useRef(null);
    const [datasetId] = useState(props.datasetId);
    const [datasetType] = useState(props.datasetType);
    useEffect(() => {
        window.$(tableRef.current).DataTable({
            searching: false,
            ordering: false,
            scrollCollapse: true,
            scrollY: 200,
            scrollX: true,
            columns: [
                { data: 'PassengerId' },
                { data: 'Survived' },
                { data: 'Pclass' },
                { data: 'Name' },
                { data: 'Sex' },
                { data: 'Age' },
                { data: 'SibSp' },
                { data: 'Parch' },
                { data: 'Ticket' },
                { data: 'Fare' },
                { data: 'Cabin' },
                { data: 'Embarked' }
            ],
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
                    console.log(d);
                    localStorage.setItem('draw', d.draw);
                    const dataSend = {
                        skip: d.start,
                        limit: d.length,
                    }
                    console.log(dataSend);
                    return dataSend
                },
                dataSrc: ""
            }
        });
    }, []);
    return (
        <div className="table-responsive">
            <table ref={tableRef} className="table nowrap w-100 no-footer">
                <thead>
                    <tr>
                        <th>PassengerId</th>
                        <th>Survived</th>
                        <th>Pclass</th>
                        <th>Name</th>
                        <th>Sex</th>
                        <th>Age</th>
                        <th>SibSp</th>
                        <th>Parch</th>
                        <th>Ticket</th>
                        <th>Fare</th>
                        <th>Cabin</th>
                        <th>Embarked</th>
                    </tr>
                </thead>
            </table>
        </div>
    );
}

export default ViewDataset;