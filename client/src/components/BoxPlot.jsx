import React, { useState, useEffect } from "react";

function BoxPlot(props) {
    const [plotType] = useState(props.plotType)
    const [columns] = useState(props.columns)
    const [data] = useState(props.visualizationDetails)

    useEffect(() => {
        var colors = ['#1abc9c', "#f672a7", "#6c757d"];
        var options = {
            series: [
                {
                    name: 'box',
                    type: 'boxPlot',
                    data: [
                        {
                            x: columns[0],
                            y: [data[columns[0]].min, data[columns[0]].q1, data[columns[0]].median, data[columns[0]].q3, data[columns[0]].max],
                        }
                    ]
                }
            ],
            chart: {
                type: 'boxPlot',
                height: 320
            },
            colors: colors,
            title: {
                text: 'Box Whisker Chart',
                align: 'left',
                style: {
                    fontSize: "14px",
                    color: '#fff'
                }
            },
            tooltip: {
                shared: false,
                intersect: true
            },
            plotOptions: {
                bar: {
                    horizontal: true
                }
            }
        };

        var chart = new window.ApexCharts(
            document.querySelector("#apex-chart"),
            options
        );

        chart.render();
    }, [])

    return (
        <div id="apex-chart">
        </div>
    );
}

export default BoxPlot;