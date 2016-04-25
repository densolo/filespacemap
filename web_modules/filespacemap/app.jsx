
import React from "react";
import ReactDOM from "react-dom";
import jquery from "jquery";

import NavBar from "filespacemap/components/navbar.jsx";
import Dashboard from "filespacemap/components/dashboard.jsx";


let App = React.createClass({
    
    getInitialState: function(){
        return {
            data: []
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
		return (
            <div>
                <NavBar title="FileSpaceMap"/>

                <Dashboard data={this.state.data}/>
		    </div>
        );
	}
});


ReactDOM.render(
	<App/>,
	document.getElementById('app-content')
);
