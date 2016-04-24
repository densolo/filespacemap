
import React from "react";
import ReactDOM from "react-dom";
import jquery from "jquery";
import filesize from "filesize";

import SpaceMap from "spacestat/components/spacemap.jsx";


// Create react components with jsx
var HelloWorld = React.createClass({
    
    getInitialState: function(){
        return {
            data: [],
            currentRect: ""
        }
    },
    
    componentDidMount: function(){
          jquery.get("../../data/data.json", function(data){
              this.setState({
                  "data": data
              })
          }.bind(this));
    },

    handleHover: function (rect){
        this.setState({
            currentRect: rect
        });
    },
    
	render: function() {
		return <div>
			<nav className="navbar navbar-default">
                <div className="container-fluid">
                    <div className="navbar-header">
                      <a className="navbar-brand" href="#">SpaceStat</a>
                    </div>
                </div>
            </nav>
            
            <SpaceMap
                data={this.state.data}
                onhover={this.handleHover}/>

            <div className="panel panel-default">
                <div className="panel-body">
                    {this.state.currentRect.size && (
                        <span className="label label-primary">{filesize(this.state.currentRect.size)}</span>
                    )}
                    {this.state.currentRect.path}
                </div>
            </div>
		</div>;
	}
});

// Render the components
ReactDOM.render(
	<HelloWorld />,
	document.getElementById('app-content')
);
