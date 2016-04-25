
import React from "react";


export default React.createClass({

    propTypes: {
        title: React.PropTypes.string.isRequired
    },
    
	render: function() {
		return (
            <nav className="navbar navbar-default">
                <div className="container-fluid">
                    <div className="navbar-header">
                      <a className="navbar-brand" href="#">{this.props.title}</a>
                    </div>
                </div>
            </nav>
        );
	}
});
