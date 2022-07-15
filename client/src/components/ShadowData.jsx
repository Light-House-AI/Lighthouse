import React, { useEffect, useRef, useState } from "react";
import axios from "axios";

function ShadowData(props) {
    const tableRef = useRef(null);
    const [projectId] = useState(props.projectId);
    const [column] = useState(props.column);

    useEffect(() => {
        axios.get(`/projects/${projectId}/columns`, {
            headers: {
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            let columnNames = response.data;
            let dtColumns = [{
                title: '#',
                data: '_id'
            }];
            window.indexPrediction = 1;

            for (let i = 0; i < columnNames.length; i++) {
                if (columnNames[i] === column) {
                    window.indexPrediction = i + 1;
                }

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
                scrollY: "40vh",
                scrollX: true,
                columns: dtColumns,
                bInfo: false,
                serverSide: true,
                processing: true,
                lengthChange: false,
                ajax: {
                    type: "GET",
                    url: `${window.baseURL}/projects/${projectId}/shadow_data`,
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
                    dataSrc: function (d) {
                        let data = [];
                        for (let i = 0; i < d.length; i++) {
                            d[i].input_data[d[i].predicted_column_name] = d[i].predicted_column_value;
                            d[i].input_data._id = d[i].id;
                            data.push(d[i].input_data);
                        }
                        return data;
                    }
                },
                "columnDefs": [
                    {
                        "targets": 0,
                        "data": "select_row",
                        "render": function (data, type, row, meta) {
                            return `<input class='form-check-input selectable-cell-predict' type='checkbox' _id=${row._id} />`;
                        }
                    }, {
                        "targets": window.indexPrediction,
                        "data": 'predicted_column_value',
                        'render': function (data, type, row, meta) {
                            return `<input type='text value='${data}' class='form-control form-control-sm' />`;
                        }
                    }]
            });
        });
    }, []);

    const createShadowData = () => {
        document.getElementById('error-div').classList.add('d-none');

        let selectedRows = window.$('#shadow-data-table .selectable-cell-predict:checked');

        if (document.getElementById('dataset-name').value === '') {
            document.getElementById('error-msg').innerHTML = 'Dataset name is required.';
            document.getElementById('error-div').classList.remove('d-none');
            return;
        }

        if (selectedRows.length === 0) {
            document.getElementById('error-msg').innerHTML = 'Please select at least one row.';
            document.getElementById('error-div').classList.remove('d-none');
            return;
        }

        let labeledData = [];
        for (let i = 0; i < selectedRows.length; i++) {
            debugger;
            labeledData.push({
                id: selectedRows[i].attributes._id.value,
                label: window.$(selectedRows[i]).parent().parent().find('.form-control.form-control-sm').val()
            });
        }

        axios.patch(`/projects/${projectId}/shadow_data`, labeledData, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
            }
        }).then((response) => {
            let shadowDataDetails = {
                project_id: projectId,
                name: document.getElementById('dataset-name').value,
            }
            axios.post(`/raw_datasets/shadow_data`, shadowDataDetails, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken')
                }
            }).then((response) => {
                window.location.href = `/${projectId}/datasets`;
            }).catch((error) => {
            });
        }).catch((error) => {
        });
    };
    return (
        <div id="shadow-data-table">
            <div className="row mb-2">
                <div className="col-9">
                    <div className="row h-100 align-items-center">
                        <div className="col-md-3 col-4 d-flex align-items-center">
                            <p className="form-label m-0">New Raw Dataset Name:</p>
                        </div>
                        <div className="col-md-3 col-4">
                            <input type="text" className="form-control" id="dataset-name" />
                        </div>
                        <div id='error-div' className="col-md-6 col-4 d-none">
                            <label id="error-msg" className="text-danger"></label>
                        </div>
                    </div>
                </div>
                <div className="col-3 text-center d-flex justify-content-end">
                    <a href={`/${projectId}/datasets`} className="btn btn-light waves-effect waves-light m-1"><i className="fe-x me-1"></i>Cancel</a>
                    <button type="button" className="btn btn-success waves-effect waves-light m-1" onClick={createShadowData}><i className="fe-check-circle me-1"></i>Create</button>
                </div>
            </div>
            <div className="table-responsive view-dataset">
                <table ref={tableRef} className="table nowrap w-100 no-footer">
                    <thead>
                    </thead>
                </table>
            </div>
        </div>
    );
}

export default ShadowData;