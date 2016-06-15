import Ember from 'ember';

export default Ember.Controller.extend({
  vehicleIndex: 0,

  visited: false,
  actions: {
    create() {
      this.transitionToRoute('register').then(function(newRoute) {
        newRoute.controller.set('access', true);
      });
    }
  }
});
