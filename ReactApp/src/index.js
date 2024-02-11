import React from 'react';
import ReactDOM from 'react-dom';
import App from "./components/App";
import {MainProvider} from "./store";


ReactDOM.render(<MainProvider><App/></MainProvider>, document.getElementById('root'));
