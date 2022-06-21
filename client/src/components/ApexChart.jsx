import React, { useState, useEffect } from "react";

function ApexChart(props) {
    const [plotType] = useState(props.plotType)
    const [columns] = useState(props.columns)
    const [visualizationDetails] = useState(props.visualizationDetails)

    useEffect(() => {
        var colors = ['#1abc9c', "#f672a7", "#6c757d"];
        var options = {
            stroke: {
                width: 5,
                curve: 'smooth'
            },
            colors: colors,
            chart: {
                height: 320,
                type: plotType,
                shadow: {
                    enabled: false,
                    color: '#bbb',
                    top: 3,
                    left: 2,
                    blur: 3,
                    opacity: 1
                },
            },
            title: {
                text: `${window.capitalizeFirstLetter(plotType)} Chart`,
                align: 'left',
                style: {
                    fontSize: "14px",
                    color: '#fff'
                }
            },
            fill: {
                type: 'gradient',
                gradient: {
                    shade: 'dark',
                    gradientToColors: colors,
                    shadeIntensity: 1,
                    type: 'horizontal',
                    opacityFrom: 1,
                    opacityTo: 1,
                    stops: [0, 100, 100, 100]
                },
            },
            markers: {
                size: 4,
                opacity: 0.9,
                colors: ["#56c2d6"],
                strokeColor: "#fff",
                strokeWidth: 2,
                style: 'inverted', // full, hollow, inverted
                hover: {
                    size: 7,
                }
            },
            grid: {
                row: {
                    colors: ['transparent', 'transparent'], // takes an array which will be repeated on columns
                    opacity: 0.2
                },
                borderColor: '#185a9d'
            },
            responsive: [{
                breakpoint: 600,
                options: {
                    chart: {
                        toolbar: {
                            show: false
                        }
                    },
                    legend: {
                        show: false
                    },
                }
            }]
        }

        if (columns.length === 2) {
            options.series = [{
                name: columns[0],
                data: visualizationDetails[columns[0]].data
            }, {
                name: columns[1],
                data: visualizationDetails[columns[1]].data
            }]
        } else {
            options.series = [{
                name: columns[0],
                data: visualizationDetails[columns[0]].data
            }]
        }

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

export default ApexChart;