
import React from "react";
import ReactDOM from "react-dom";
import Dashboard from "spacestat/components/dashboard.jsx";


// Create react components with jsx
var HelloWorld = React.createClass({
	render: function() {
		return <div>
			<h1>Hello World</h1>
            <Dashboard data={[1,2,3]}/>
		</div>;
	}
});

// Render the components
ReactDOM.render(
	<HelloWorld />,
	document.getElementById('app-content')
);
