import React from 'react';
import {
  Route,
} from 'react-router';
import {BrowserRouter,Switch} from 'react-router-dom';
import App from './components/App'

const Routes = () => (
  <BrowserRouter>
    <Switch>
      <Route path="/" component={App} />
    </Switch>

  </BrowserRouter>
);

export default Routes;