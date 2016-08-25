import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
    location: config.locationType,
    rootURL: config.rootURL
});

Router.map(function() {
  this.route('conference', { path: '/conference' }, function() {
      this.route('index', { path: '/:conference_id' });
      this.route('new');
      this.route('submission', { path: '/:conference_id/submission' });
  });
  this.route('login');
  this.route('signup');
  this.route('search');

  this.route('logout');
});

export default Router;
