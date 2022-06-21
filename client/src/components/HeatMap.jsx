import React, { useState, useEffect } from "react";

function HeatMap(props) {
    const [plotType] = useState(props.plotType)
    const [data] = useState(props.visualizationDetails)

    useEffect(() => {
        var colors = ['#1abc9c'];
        var options = {
            colors: colors,
            series: [],
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
            dataLabels: {
                enabled: false
            },
            title: {
                text: `${window.capitalizeFirstLetter(plotType)} Chart`,
                align: 'left',
                style: {
                    fontSize: "14px",
                    color: '#fff'
                }
            },
            xaxis: {
                categories: Object.keys(data)
            },
            plotOptions: {
                heatmap: {
                    min: -1,
                    max: 1
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
        };

        for (let i = 0; i < Object.keys(data).length; i++) {
            debugger
            options.series.push({
                name: Object.keys(data)[i],
                data: Object.values(data[Object.keys(data)[i]])
            })
        }

        console.log(options.series);

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

export default HeatMap;