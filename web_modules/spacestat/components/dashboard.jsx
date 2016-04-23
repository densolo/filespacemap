
import React from "react";
import ReactFauxDOM from "react-faux-dom";
import d3 from "d3";
import _ from "lodash";


export default React.createClass({

    propTypes: {
        data: React.PropTypes.array
    },

    getInitialState: function(){
        return {
            width: 100,
            height: 100
        };
    },

    componentDidMount: function(){
        this.updateSizes(this.props.data);
    },

    componentWillReceiveProps: function (newProps) {
        let props = _.merge(this.props, newProps);
        this.updateSizes(props.data);
    },

    updateSizes: function(data){
        if (!data || data.length == 0){
            return;
        }

        data.forEach(function(d){
           console.log("x: " + d.x + ", y: " + d.y + ", dx: " + d.dx + ", dy: " + d.dy);
        });

        let w = _.maxBy(this.props.data, function(d){ return d.x + d.dx; });
        let h = _.maxBy(this.props.data, function(d){ return d.y + d.dy; });

        this.setState({
            width: w.x + w.dx,
            height: h.y + h.dy
        })
    },

    render: function () {
        let view = ReactFauxDOM.createElement('div');

        let svg = d3.select(view)
            .append("svg")
            .attr("width", this.state.width)
            .attr("height", this.state.height);

        let rectUpdate = svg.selectAll("rect").data(this.props.data);

        rectUpdate.enter()
            .append("rect")
            .attr("x", function(d){ return d.x; })
            .attr("y", function(d){ return d.y; })
            .attr("width", function(d){ return _.max([d.dx - 1, 0]); })
            .attr("height", function(d){ return _.max([d.dy - 1, 0]); })
            .style("fill", "blue");

        let textUpdate = svg.selectAll("text").data(this.props.data);

        textUpdate.enter()
            .append("text")
            .attr("x", function(d){ return d.x + 2; })
            .attr("y", function(d){ return d.y + 20; })
            .text(function(d) { return d.name; });


        // .style("width", function(d) { return d * 10 + "px"; })
        //     .style("background-color", "lightgrey")
        //     .text(function (d) {
        //         return d
        //     });

        return view.toReact();
    }
});
