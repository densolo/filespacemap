
import React from "react";
import ReactFauxDOM from "react-faux-dom";
import d3 from "d3";


export default React.createClass({

    propTypes: {
        data: React.PropTypes.array
    },

    render: function () {
        let view = ReactFauxDOM.createElement('div');

        d3.select(view)
            .selectAll('div')
            .data(this.props.data) // 1, 2, 3...
            .enter()
            .append("div")
            .style("width", function(d) { return d * 10 + "px"; })
            .style("background-color", "lightgrey")
            .text(function (d) {
                return d
            });

        return view.toReact();

    }
});
