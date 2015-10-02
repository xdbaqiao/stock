var gridbordercolor = "#eee";
var InitiateFlotSelectableChart = function () {
    return {
        init: function () {

            var data = [{
                color: themeprimary,
                label: "Windows",
                data: [[1970, 18.9], [1991, 18.7], [1992, 18.4], [1993, 19.3], [1994, 19.5], [1995, 19.3], [1996, 19.4], [1997, 20.2], [1998, 19.8], [1999, 19.9], [2000, 20.4], [2001, 20.1], [2002, 20.0], [2003, 19.8], [2004, 20.4]]
            }
            , {
                color: themethirdcolor,
                label: "Linux",
                data: [[1970, 10.0], [1991, 11.3], [1992, 9.9], [1993, 9.6], [1994, 9.5], [1995, 9.5], [1996, 9.9], [1997, 9.3], [1998, 9.2], [1999, 9.2], [2000, 9.5], [2001, 9.6], [2002, 9.3], [2003, 9.4], [2004, 9.79]]
            }
            , {
                color: themesecondary,
                label: "Mac OS",
                data: [[1970, 5.8], [1991, 6.0], [1992, 5.9], [1993, 5.5], [1994, 5.7], [1995, 5.3], [1996, 6.1], [1997, 5.4], [1998, 5.4], [1999, 5.1], [2000, 5.2], [2001, 5.4], [2002, 6.2], [2003, 5.9], [2004, 5.89]]
            }, {
                color: themefourthcolor,
                label: "DOS",
                data: [[1970, 8.3], [1991, 8.3], [1992, 7.8], [1993, 8.3], [1994, 8.4], [1995, 5.9], [1996, 6.4], [1997, 6.7], [1998, 6.9], [1999, 7.6], [2000, 7.4], [2001, 8.1], [2002, 12.5], [2003, 9.9], [2004, 19.0]]
            }];

            var options = {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                legend: {
                    noColumns: 4
                },
                xaxis: {
                    tickDecimals: 0,
                    color: gridbordercolor,
					ticks: [1970, 1991]
                },
                yaxis: {
                    min: 0,
                    color: gridbordercolor
                },
                selection: {
                    mode: "x"
                },
                grid: {
                    hoverable: true,
                    clickable: false,
                    borderWidth: 0,
                    aboveData: false
                },
                tooltip: true,
                tooltipOpts: {
                    defaultTheme: false,
                    content: "<b>%s</b> : <span>%x</span> : <span>%y</span>",
                },
                crosshair: {
                    mode: "x"
                }
            };

            var placeholder = $("#selectable-chart");

            placeholder.bind("plotselected", function (event, ranges) {

                var zoom = $("#zoom").is(":checked");

                if (zoom) {
                    plot = $.plot(placeholder, data, $.extend(true, {}, options, {
                        xaxis: {
                            min: ranges.xaxis.from,
                            max: ranges.xaxis.to
                        }
                    }));
                }
            });

            placeholder.bind("plotunselected", function (event) {
                // Do Some Work
            });

            var plot = $.plot(placeholder, data, options);

            $("#clearSelection").click(function () {
                plot.clearSelection();
            });

            $("#setSelection").click(function () {
                plot.setSelection({
                    xaxis: {
                        from: 1994,
                        to: 1995
                    }
                });
            });
        }
    };
}();

