import React, { useState, useEffect } from "react";

function ApexChart(props) {
    const [plotType] = useState(props.plotType)
    const [columns] = useState(props.columns)

    useEffect(() => {
        var colors = ['#f672a7'];
        var options = {
            stroke: {
                width: 5,
                curve: 'smooth'
            },
            series: [{
                name: columns[0],
                data: [4, 3, 10, 9, 29, 19, 22, 9, 12, 7, 19, 5, 13, 9, 17, 2, 7, 5]
            }],
            xaxis: {
                type: 'datetime',
                categories: ['1/11/2000', '2/11/2000', '3/11/2000', '4/11/2000', '5/11/2000', '6/11/2000', '7/11/2000', '8/11/2000', '9/11/2000', '10/11/2000', '11/11/2000', '12/11/2000', '1/11/2001', '2/11/2001', '3/11/2001', '4/11/2001', '5/11/2001', '6/11/2001'],
            },
            yaxis: {
                min: -10,
                max: 40,
                title: {
                    text: columns[1],
                },
            },
            chart: {
                height: 380,
                type: 'line',
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
                text: plotType,
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