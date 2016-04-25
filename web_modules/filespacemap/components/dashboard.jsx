
import React from "react";
import filesize from "filesize";
import _ from "lodash";

import SpaceMap from "filespacemap/components/spacemap.jsx";


export default React.createClass({

    propTypes: {
        data: React.PropTypes.array
    },

    getInitialState: function(){
        return {
            currentRect: "",
            selectedRects: []
        }
    },

    _handleHover: function (rect){
        this.setState({
            currentRect: rect
        });
    },

    _handleClick: function (rect){
        let newSelection = _.filter(this.state.selectedRects, function(r){return r.path != rect.path;});
        if (newSelection.length == this.state.selectedRects.length) {
            newSelection.push(rect);
        }
        this.setState({
            selectedRects: newSelection
        });
    },
    
	render: function() {
		return (
            <div>
                <SpaceMap
                    data={this.props.data}
                    selection={this.state.selectedRects}
                    onhover={this._handleHover}
                    onclick={this._handleClick}/>

                <div className="panel panel-default">
                    <div className="panel-body selected-paths">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th></th>
                                    <th>Size</th>
                                    <th>Path</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td></td>
                                    <td>
                                        <span className="label label-primary">{this.state.currentRect.size && filesize(this.state.currentRect.size)}</span>
                                    </td>
                                    <td>{this.state.currentRect.path}</td>
                                </tr>
                                {this.state.selectedRects.map(function(rect, i){
                                  return (
                                      <tr key={i}>
                                          <td>{i+1}</td>
                                          <td>{rect.size && filesize(rect.size)}</td>
                                          <td>{rect.path}</td>
                                      </tr>
                                  );
                                })}
                            </tbody>
                        </table>
                    </div>
                </div>
		    </div>
        );
	}
});
