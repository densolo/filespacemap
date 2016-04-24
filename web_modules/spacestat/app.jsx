
import React from "react";
import ReactDOM from "react-dom";
import jquery from "jquery";

import Dashboard from "spacestat/components/dashboard.jsx";


// Create react components with jsx
var HelloWorld = React.createClass({
    
    getInitialState: function(){
        return {
            data: [],
            currentRect: ""
        }
    },
    
    componentDidMount: function(){
          jquery.get("../data/data.json", function(data){
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
			<h1>SpaceStat</h1>
            <Dashboard
                data={this.state.data}
                onhover={this.handleHover}/>
            <label>{this.state.currentRect.path}</label>
		</div>;
	}
});

// Render the components
ReactDOM.render(
	<HelloWorld />,
	document.getElementById('app-content')
);
